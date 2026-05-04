"""Tests for VB6 extraction (extract_vb6). All tests RED until extract_vb6 is implemented."""
from pathlib import Path

import pytest

from graphify.extract import _make_id, extract_vb6, _DISPATCH
from graphify.detect import CODE_EXTENSIONS

FIXTURES = Path(__file__).parent / "fixtures"


# ── dispatch / detection ──────────────────────────────────────────────────────

def test_dispatch_registers_bas():
    assert ".bas" in _DISPATCH


def test_dispatch_registers_cls():
    assert ".cls" in _DISPATCH


def test_dispatch_registers_frm():
    assert ".frm" in _DISPATCH


def test_code_extensions_includes_bas():
    assert ".bas" in CODE_EXTENSIONS


def test_code_extensions_includes_cls():
    assert ".cls" in CODE_EXTENSIONS


def test_code_extensions_includes_frm():
    assert ".frm" in CODE_EXTENSIONS


# ── basic .bas structure ──────────────────────────────────────────────────────

def test_extract_vb6_bas_returns_nodes_and_edges():
    result = extract_vb6(FIXTURES / "sample.bas")
    assert "nodes" in result
    assert "edges" in result


def test_extract_vb6_bas_file_node_emitted():
    result = extract_vb6(FIXTURES / "sample.bas")
    labels = [n["label"] for n in result["nodes"]]
    assert "sample.bas" in labels


def test_extract_vb6_bas_finds_functions():
    result = extract_vb6(FIXTURES / "sample.bas")
    labels = [n["label"] for n in result["nodes"]]
    assert any("Add" in l for l in labels)
    assert any("Multiply" in l for l in labels)


def test_extract_vb6_bas_finds_subs():
    result = extract_vb6(FIXTURES / "sample.bas")
    labels = [n["label"] for n in result["nodes"]]
    assert any("PrintResult" in l for l in labels)


def test_extract_vb6_bas_contains_edges():
    result = extract_vb6(FIXTURES / "sample.bas")
    contains = [e for e in result["edges"] if e["relation"] == "contains"]
    assert len(contains) >= 3  # file → Add, Multiply, PrintResult


def test_extract_vb6_bas_contains_edges_confidence():
    result = extract_vb6(FIXTURES / "sample.bas")
    for edge in result["edges"]:
        if edge["relation"] == "contains":
            assert edge["confidence"] == "EXTRACTED"


def test_extract_vb6_bas_no_dangling_edges():
    result = extract_vb6(FIXTURES / "sample.bas")
    node_ids = {n["id"] for n in result["nodes"]}
    for edge in result["edges"]:
        assert edge["source"] in node_ids, f"Dangling source: {edge}"


def test_extract_vb6_bas_source_file_set():
    result = extract_vb6(FIXTURES / "sample.bas")
    for node in result["nodes"]:
        assert "source_file" in node
    for edge in result["edges"]:
        assert "source_file" in edge


def test_extract_vb6_bas_source_location_set():
    result = extract_vb6(FIXTURES / "sample.bas")
    non_file_nodes = [n for n in result["nodes"] if n["label"] != "sample.bas"]
    assert all("source_location" in n for n in non_file_nodes)


# ── call graph (.bas) ─────────────────────────────────────────────────────────

def test_extract_vb6_calls_edges_emitted():
    result = extract_vb6(FIXTURES / "sample_calls.bas")
    calls = [e for e in result["edges"] if e["relation"] == "calls"]
    assert len(calls) > 0


def test_extract_vb6_calls_confidence_extracted():
    result = extract_vb6(FIXTURES / "sample_calls.bas")
    for edge in result["edges"]:
        if edge["relation"] == "calls":
            assert edge["confidence"] == "EXTRACTED"
            assert edge["weight"] == 1.0


def test_extract_vb6_calls_context():
    result = extract_vb6(FIXTURES / "sample_calls.bas")
    for edge in result["edges"]:
        if edge["relation"] == "calls":
            assert edge.get("context") == "call"


def test_extract_vb6_calls_no_self_loops():
    result = extract_vb6(FIXTURES / "sample_calls.bas")
    for edge in result["edges"]:
        if edge["relation"] == "calls":
            assert edge["source"] != edge["target"], f"Self-loop: {edge}"


def test_extract_vb6_runanalysis_calls_computescore():
    result = extract_vb6(FIXTURES / "sample_calls.bas")
    calls = {(e["source"], e["target"]) for e in result["edges"] if e["relation"] == "calls"}
    node_by_label = {n["label"]: n["id"] for n in result["nodes"]}
    src = next((v for k, v in node_by_label.items() if "RunAnalysis" in k), None)
    tgt = next((v for k, v in node_by_label.items() if "ComputeScore" in k), None)
    assert src and tgt, f"Node not found. labels={list(node_by_label)}"
    assert (src, tgt) in calls


def test_extract_vb6_runanalysis_calls_normalize():
    result = extract_vb6(FIXTURES / "sample_calls.bas")
    calls = {(e["source"], e["target"]) for e in result["edges"] if e["relation"] == "calls"}
    node_by_label = {n["label"]: n["id"] for n in result["nodes"]}
    src = next((v for k, v in node_by_label.items() if "RunAnalysis" in k), None)
    tgt = next((v for k, v in node_by_label.items() if "Normalize" in k), None)
    assert src and tgt
    assert (src, tgt) in calls


def test_extract_vb6_calls_deduplication():
    result = extract_vb6(FIXTURES / "sample_calls.bas")
    call_pairs = [(e["source"], e["target"]) for e in result["edges"] if e["relation"] == "calls"]
    assert len(call_pairs) == len(set(call_pairs)), "Duplicate calls edges"


# ── .cls class module ─────────────────────────────────────────────────────────

def test_extract_vb6_cls_file_node_emitted():
    result = extract_vb6(FIXTURES / "sample.cls")
    labels = [n["label"] for n in result["nodes"]]
    assert "sample.cls" in labels


def test_extract_vb6_cls_finds_class_node():
    result = extract_vb6(FIXTURES / "sample.cls")
    labels = [n["label"] for n in result["nodes"]]
    assert any("sample" in l.lower() for l in labels if l != "sample.cls")


def test_extract_vb6_cls_finds_methods():
    result = extract_vb6(FIXTURES / "sample.cls")
    labels = [n["label"] for n in result["nodes"]]
    assert any("Initialize" in l for l in labels)
    assert any("GetGreeting" in l for l in labels)


def test_extract_vb6_cls_no_dangling_edges():
    result = extract_vb6(FIXTURES / "sample.cls")
    node_ids = {n["id"] for n in result["nodes"]}
    for edge in result["edges"]:
        assert edge["source"] in node_ids, f"Dangling source: {edge}"
