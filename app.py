import streamlit as st
import numpy as np
import json
from dataclasses import asdict
from finalysis.instruments import Option, Spot, Future, Sum, Instrument
from finalysis import plot

st.set_page_config(page_title="Finalysis", layout="wide")
st.title("📈 Finalysis Strategy Builder")



# --- Init state ---
if "strategy" not in st.session_state:
    st.session_state.strategy = []

# --- Layout ---
left, right = st.columns([1, 2])

with left:
    st.subheader("📦 Strategy Editor")

    def instrument_form(key: str) -> Instrument | None:
        kind = st.selectbox("Type", ["Option", "Spot", "Future", "SellHighDI", "BuyLowDI", "SmartLeverage"], key=key)
        quantity = st.number_input("Quantity", value=1.0, key=key + "_qty")

        if kind == "Option":
            strike = st.number_input("Strike", value=635.0, key=key + "_strike")
            premium = st.number_input("Premium", value=7.0, key=key + "_prem")
            opt_type = st.selectbox("Kind", ["call", "put"], key=key + "_type")
            return Option(strike=strike, premium=premium, kind=opt_type, quantity=quantity)

        if kind == "Spot":
            price = st.number_input("Buy Price", value=635.0, key=key + "_price")
            return Spot(price=price, quantity=quantity)

        if kind == "Future":
            entry = st.number_input("Entry Price", value=635.0, key=key + "_entry")
            ftype = st.selectbox("Kind", ["long", "short"], key=key + "_ftype")
            return Future(price=entry, kind=ftype, quantity=quantity)

        return None

    if st.button("Reset Strategy"):
        st.session_state.strategy.clear()

    for i, inst in enumerate(st.session_state.strategy):
        label = f"#{i+1}: {type(inst).__name__} - {', '.join(f'{k}={v}' for k,v in asdict(inst).items())}"
        with st.expander(label):
            updated = instrument_form(f"edit_{i}")
            cols = st.columns([1, 1])
            if cols[0].button("Update", key=f"update_{i}"):
                st.session_state.strategy[i] = updated
            if cols[1].button("Delete", key=f"delete_{i}"):
                del st.session_state.strategy[i]
                st.rerun()

    with st.expander("➕ Add New Instrument"):
        new_instr = instrument_form("new")
        if st.button("Add", key="add_new") and new_instr:
            st.session_state.strategy.append(new_instr)
            st.rerun()

    # JSON editor field
    json_input = st.text_area(
        "📄 Strategy JSON",
        value=json.dumps([
            {**asdict(i), "type": type(i).__name__} for i in st.session_state.strategy
        ], indent=2),
        height=200,
        key="strategy_json"
    )

    try:
        parsed = json.loads(json_input)
        type_map = {
            "Option": Option,
            "Spot": Spot,
            "Future": Future,
        }
        st.session_state.strategy = [type_map[item.pop("type")](**item) for item in parsed]
    except Exception:
        st.caption("(Invalid JSON — won't apply until it's fixed)")

with right:
    st.subheader("📊 Payoff Plot")
    price = st.number_input("Current Price", value=635.0, key="cfg_price")

    if st.session_state.strategy:
        strategy = Sum(st.session_state.strategy)
        fig = plot.payoff(strategy, price)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add instruments to build a strategy and view its payoff.")

    with st.expander("⚙️ Plot Settings"):
        min_price = st.number_input("Min Final Price", value=0.95 * price, key="cfg_min")
        max_price = st.number_input("Max Final Price", value=1.05 * price, key="cfg_max")
        steps = st.slider("Steps", 100, 2000, 1000, key="cfg_steps")
        relative = st.checkbox("Show Relative PnL", value=False, key="cfg_rel")

        if st.session_state.strategy:
            fig = plot.payoff(
                strategy,
                price,
                min_price=min_price,
                max_price=max_price,
                steps=steps,
                relative=relative
            )
            st.plotly_chart(fig, use_container_width=True)
