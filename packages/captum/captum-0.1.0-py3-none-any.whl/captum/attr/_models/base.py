#!/usr/bin/env python3

import torch

import warnings

from functools import reduce
from torch.nn import Embedding


class InterpretableEmbeddingBase(Embedding):
    r"""
        Since some embedding vectors, e.g. word are created and assigned in
        the embedding layers of Pytorch models we need a way to access
        those layers, generate the embeddings and subtract the baseline.
        To do so, we separate embedding layers from the model, compute the
        embeddings separately and do all operations needed outside of the model.
        The original embedding layer is being replaced by
        `InterpretableEmbeddingBase` layer which passes already
        precomputed embedding vectors to the layers below.
    """

    def __init__(self, embedding, full_name):
        super().__init__(embedding.num_embeddings, embedding.embedding_dim)
        self.embedding = embedding
        self.full_name = full_name

    def forward(self, input):
        r"""
         The forward function of a wrapper embedding layer that takes and returns
         embedding layer. It allows embeddings to be created outside of the model
         and passes them seamlessly to the preceding layers of the model.

         Args

            inputs (tensor): Input embedding tensor containing the embedding vectors
                    of each word or token in the sequence.

         Return

            output (tensor): Returns output tensor which is the same as input tensor.
                   It passes embedding tensors to lower layers without any
                   modifications.
        """
        return input

    def indices_to_embeddings(self, input):
        r"""
        Maps indices to corresponding embedding vectors. E.g. word embeddings

        Args

            input (tensor): A tensor of input indices. A typical example of an
                   input index is word or token index.

        Returns

            embedding (tensor): A tensor of word embeddings corresponding to the
                    indices specified in the input
        """
        return self.embedding(input)


class TokenReferenceBase:
    r"""
    A base class for creating reference (aka baseline) tensor for a sequence of
    tokens. A typical example of such token is `PAD`. Users need to provide the
    index of the reference token in the vocabulary as an argument to
    `TokenReferenceBase` class.
    """

    def __init__(self, reference_token_idx=0):
        self.reference_token_idx = reference_token_idx

    def generate_reference(self, sequence_length, device):
        r"""
        Generated reference tensor of given `sequence_length` using
        `reference_token_idx`.

        Args
            sequence_length (int): The length of the reference sequence
            device (torch.device): The device on which the reference tensor will
                          be created.
        Returns

            reference (tensor): A sequence of reference token with shape:
                          [sequence_length]
        """
        return torch.tensor([self.reference_token_idx] * sequence_length, device=device)


def _get_deep_layer_name(obj, layer_names):
    r"""
    Traverses through the layer names that are separated by
    dot in order to access the embedding layer.
    """
    return reduce(getattr, layer_names.split("."), obj)


def _set_deep_layer_value(obj, layer_names, value):
    r"""
    Traverses through the layer names that are separated by
    dot in order to access the embedding layer and update its value.
    """
    layer_names = layer_names.split(".")
    setattr(reduce(getattr, layer_names[:-1], obj), layer_names[-1], value)


def configure_interpretable_embedding_layer(model, embedding_layer_name="embedding"):
    r"""
    This method wraps model's embedding layer with an interpretable embedding
    layer that allows us to access the embeddings through their indices.

    Args

        model (torch.nn.Model): An instance of PyTorch model that contains embeddings.
        embedding_layer_name (str, optional): The name of the embedding layer
                    in the `model` that we would like to make interpretable.

    Returns

        interpretable_emb (tensor): An instance of `InterpretableEmbeddingBase`
                    embedding layer that wraps model's embedding layer that is being
                    accessed through `embedding_layer_name`.

    Examples::

                >>> # Let's assume that we have a DocumentClassifier model that
                >>> # has a word embedding layer named 'embedding'.
                >>> # To make that layer interpretable we need to execute the
                >>> # following command:
                >>> net = DocumentClassifier()
                >>> interpretable_emb = configure_interpretable_embedding_layer(net,
                >>>    'embedding')
                >>> # then we can use interpretable embedding to convert our
                >>> # word indices into embeddings.
                >>> # Let's assume that we have the following word indices
                >>> input_indices = torch.tensor([1, 0, 2])
                >>> # we can access word embeddings for those indices with the command
                >>> # line stated below.
                >>> input_emb = interpretable_emb.indices_to_embeddings(input_indices)
                >>> # Let's assume that we want to apply integrated gradients to
                >>> # our model and that target attribution class is 3
                >>> ig = IntegratedGradients(net)
                >>> attribution = ig.attribute(input_emb, target=3)
                >>> # after we finish the interpretation we need to remove
                >>> # interpretable embedding layer with the following command:
                >>> remove_interpretable_embedding_layer(net, interpretable_emb)

    """
    embedding_layer = _get_deep_layer_name(model, embedding_layer_name)
    assert (
        embedding_layer.__class__ is not InterpretableEmbeddingBase
    ), "InterpretableEmbeddingBase has already been configured for layer {}".format(
        embedding_layer_name
    )
    warnings.warn(
        """In order to make embedding layers more interpretable they will
        be replaced with an interpretable embedding layer which wraps the
        original embedding layer and takes word embedding vectors as inputs of
        the forward function. This allows to generate baselines for word
        embeddings and compute attributions for each embedding dimension.
        The original embedding layer must be set
        back by calling `remove_interpretable_embedding_layer` function
        after model interpretation is finished."""
    )
    interpretable_emb = InterpretableEmbeddingBase(
        embedding_layer, embedding_layer_name
    )
    _set_deep_layer_value(model, embedding_layer_name, interpretable_emb)
    return interpretable_emb


def remove_interpretable_embedding_layer(model, interpretable_emb):
    r"""
    Removes interpretable embedding layer and sets back original
    embedding layer in the model.

    Args

        model (torch.nn.Module): An instance of PyTorch model that contains embeddings
        interpretable_emb (tensor): An instance of `InterpretableEmbeddingBase`
                    that was originally created in
                    `configure_interpretable_embedding_layer` function and has
                    to be removed after interpretation is finished.

    Examples::

                >>> # Let's assume that we have a DocumentClassifier model that
                >>> # has a word embedding layer named 'embedding'.
                >>> # To make that layer interpretable we need to execute the
                >>> # following command:
                >>> net = DocumentClassifier()
                >>> interpretable_emb = configure_interpretable_embedding_layer(net,
                >>>    'embedding')
                >>> # then we can use interpretable embedding to convert our
                >>> # word indices into embeddings.
                >>> # Let's assume that we have the following word indices
                >>> input_indices = torch.tensor([1, 0, 2])
                >>> # we can access word embeddings for those indices with the command
                >>> # line stated below.
                >>> input_emb = interpretable_emb.indices_to_embeddings(input_indices)
                >>> # Let's assume that we want to apply integrated gradients to
                >>> # our model and that target attribution class is 3
                >>> ig = IntegratedGradients(net)
                >>> attribution = ig.attribute(input_emb, target=3)
                >>> # after we finish the interpretation we need to remove
                >>> # interpretable embedding layer with the following command:
                >>> remove_interpretable_embedding_layer(net, interpretable_emb)

    """
    _set_deep_layer_value(
        model, interpretable_emb.full_name, interpretable_emb.embedding
    )
