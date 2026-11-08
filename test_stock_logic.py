# Regression test scenarios for V104 stock handling.
# Run in a configured Python environment with pytest and the app dependencies installed.
#
# 1) Stock 10 + confirmed quantity 1 => stock 9; product row remains.
# 2) Stock 1 + confirmed quantity 1 => stock 0; product row remains and storefront shows Out of Stock.
# 3) Re-confirming the same order does not deduct stock twice (`stock_deducted` flag).
# 4) Insufficient stock blocks confirmation and leaves inventory unchanged.
#
# The production function under test is confirm_order_and_deduct_stock() in app.py.
