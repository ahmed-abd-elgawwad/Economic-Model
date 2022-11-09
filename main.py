import streamlit as st
import pandas as pd
import numpy_financial as npf
import plotly_express as px
st.markdown("""
# __Economic model__
- upload the __NCF__ file 
- calculate the __NPV__ 
- calculate the __DCFROR__

""")
st.sidebar.markdown("## __Input parameters__")
file = st.sidebar.file_uploader("Upload NCF File",type=["xlsx"])
ir = st.sidebar.number_input("Annual Interset Rate (%)")

### working with the file
if file:
    df = pd.read_excel(file)
    df["PV"] = df.NCF / (1+(ir/100))**df.year
    df = df.round(2)
    st.table(df)
    # get the NPV
    NPV = round(npf.npv(ir/100,df["NCF"] ),3)
    # get the IRR
    IRR = round(npf.irr(df["NCF"]) *100, 3)
    # show the parametes
    col1 ,col2 = st.columns(2)
    with col1:
        st.metric("NPV", NPV)
    with col2:
        st.metric("DCFROR",str(IRR)+ " %")

    # ---------------------- graphing ----------------------------
    st.write("## __Draw graphs__")
    st.write("##### 1 | Year Vs ( NCF & PV )")
    cols = list(df.columns)
    col1, col2 ,col3 = st.columns(3)
    with col1:
        c1 = st.selectbox("X-axis",cols)
    with col2:
        c2 = st.selectbox("Y-axis", cols)
    with col3:
        c3 = st.selectbox("Graph_Type",["bar","line"])
    if c3 =="bar":
        fig = px.bar(data_frame=df,x=c1,y=c2)
    else:
        fig = px.line(data_frame=df, x=c1, y=c2)
    st.plotly_chart(fig, use_container_width=True)

   # the NPV vs the Ir
    st.write("##### 2| Initial rate Vs NPV")
    col1, col2, col3 = st.columns(3)
    with col1:
         initial_rate = st.number_input("initial rate")
    with col2:
        inc = st.number_input("increment")
    with col3:
        points = st.number_input("Num of Points",min_value=1)
    rs = [initial_rate]
    for i in range(1,int(points)):
        k = round(rs[i-1] + inc , 3)
        rs.append(k)

    # calulate the NPv for each ir
    NPVs = [ round(npf.npv(r/100, df["NCF"]), 3) for r in rs ]
    fig = px.line(x=rs,y=NPVs,labels={"x":"Rate Ir","y":"NPV"})
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=rs,
        )
    )
    fig.add_vline(x=IRR)
    st.plotly_chart(fig, use_container_width=True)

    # st.write(rs)

