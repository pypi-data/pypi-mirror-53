# -*- coding: utf-8 -*-

"""Testing for CX and NDEx import/export."""

import os
import tempfile

from pybel import BELGraph
from pybel.examples import braf_graph, egf_graph, sialic_acid_graph, statin_graph

from pybel_cx.cx import from_cx, from_cx_file, from_cx_jsons, to_cx, to_cx_file, to_cx_jsons
from tests.cases import TestCase
from tests.examples import example_graph


class TestSchema1(TestCase):
    """Test mapping schema 1."""

    def help_test_graph(self, graph: BELGraph) -> None:
        """Help test a graph round trip through a JSON object."""
        graph_cx = to_cx(graph)
        reconstituted = from_cx(graph_cx)
        self.assert_graph_equal(graph, reconstituted)

    def help_test_jsons(self, graph: BELGraph) -> None:
        """Help test a graph round trip through a JSON string."""
        graph_cx_str = to_cx_jsons(graph)
        reconstituted = from_cx_jsons(graph_cx_str)
        self.assert_graph_equal(graph, reconstituted)

    def help_test_file(self, graph: BELGraph) -> None:
        """Help test a graph round trip through a file."""
        fd, path = tempfile.mkstemp()

        with open(path, 'w') as file:
            to_cx_file(graph, file)

        with open(path) as file:
            reconstituted = from_cx_file(file)

        self.assert_graph_equal(graph, reconstituted)

        os.close(fd)
        os.remove(path)

    def test_sialic_acid_graph(self):
        """Test the round trip in the sialic acid graph."""
        self.help_test_graph(sialic_acid_graph)

    def test_braf_graph(self):
        """Test the round trip in the BRAF graph."""
        self.help_test_graph(braf_graph)

    def test_egf_graph(self):
        """Test the round trip in the EGF graph."""
        self.help_test_graph(egf_graph)

    def test_statin_graph(self):
        """Test the round trip in the statin graph."""
        self.help_test_graph(statin_graph)

    def test_example(self):
        """Test the round trip in an example graph."""
        self.help_test_graph(example_graph)

    def test_example_jsons(self):
        """Test the round trip to a JSON string with the example graph."""
        self.help_test_graph(example_graph)

    def test_example_file(self):
        """Test the round trip to a file with the example graph."""
        self.help_test_file(example_graph)
