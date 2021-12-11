from datetime import date, timedelta
import pytest
from model import allocate, OrderLine, Batch, OutOfStock

def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", sku, batch_qty, eta=date.today()),
        OrderLine("order-123", sku, line_qty)
    )

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine('123', "SMALL-TABLE", 10)
    batch.allocate(line)
    assert batch.available_quantity == 10

def test_not_allowed_to_allocate_to_a_batch_with_less_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=2, eta=date.today())
    line = OrderLine('123', "SMALL-TABLE", 10)
    batch.allocate(line)
    assert batch.available_quantity == 2

def test_cannot_allocate_the_same_line_twice():
    # also known as checking idempotent = reprocessing the same thing will not change anything
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine('123', "SMALL-TABLE", 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18

def test_cannot_allocate_if_skus_dont_match():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine('123', "BLUE-CUSHION", 2)
    assert batch.can_allocate(line) == False

def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20 