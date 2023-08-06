#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# @file   test_generate.py
# @author Albert Puig (albert.puig@cern.ch)
# @date   27.02.2019
# =============================================================================
"""Basic dimensionality tests."""

import pytest

import tensorflow as tf

import phasespace

import os
import sys

sys.path.append(os.path.dirname(__file__))

from .helpers import decays

B0_MASS = decays.B0_MASS
PION_MASS = decays.PION_MASS


def setup_method():
    phasespace.GenParticle._sess.close()
    tf.reset_default_graph()


def test_one_event():
    """Test B->pi pi pi."""
    decay = phasespace.nbody_decay(B0_MASS, [PION_MASS, PION_MASS, PION_MASS])
    norm_weights, particles = decay.generate(n_events=1)
    assert len(norm_weights) == 1
    assert all([weight < 1 for weight in norm_weights])
    assert len(particles) == 3
    assert all([part.shape == (1, 4) for part in particles.values()])


def test_one_event_tf():
    """Test B->pi pi pi."""
    decay = phasespace.nbody_decay(B0_MASS, [PION_MASS, PION_MASS, PION_MASS])
    with tf.Session() as sess:
        norm_weights, particles = sess.run(decay.generate_tensor(n_events=1))

    assert len(norm_weights) == 1
    assert all([weight < 1 for weight in norm_weights])
    assert len(particles) == 3
    assert all([part.shape == (1, 4) for part in particles.values()])


@pytest.mark.parametrize("n_events", argvalues=[5])
def test_n_events(n_events):
    """Test 5 B->pi pi pi."""
    decay = phasespace.nbody_decay(B0_MASS, [PION_MASS, PION_MASS, PION_MASS])
    norm_weights, particles = decay.generate(n_events=n_events)
    assert len(norm_weights) == 5
    assert all([weight < 1 for weight in norm_weights])
    assert len(particles) == 3
    assert all([part.shape == (5, 4) for part in particles.values()])


def test_cache():
    from phasespace import GenParticle

    mother_particle = GenParticle('mother', 10000)
    daughter1 = GenParticle('daughter1', mass=2000)
    _ = mother_particle.set_children(daughter1, GenParticle('daughter2', mass=1000))
    assert not mother_particle._cache_valid
    _ = mother_particle.generate(n_events=8)
    tensor1 = mother_particle._cache
    _ = mother_particle.generate(n_events=5)
    tensor1_too = mother_particle._cache
    assert tensor1 is tensor1_too
    assert mother_particle._cache is not None
    assert mother_particle._cache_valid

    daughter1.set_children(GenParticle('daugther21', mass=100),
                           GenParticle('daughter22', mass=500))
    assert not mother_particle._cache_valid
    _ = mother_particle.generate(n_events=3)
    tensor2 = mother_particle._cache
    assert tensor2 is not tensor1
    assert mother_particle._cache_valid


if __name__ == "__main__":
    test_one_event()
    test_n_events(5)

    # EOF
