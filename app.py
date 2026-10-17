import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium", app_title="Bienes Raíces - Dubai")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bienes Raíces (Dubai)
    """)
    return


@app.cell(hide_code=True)
def _():
    import pandas as pd
    import numpy as np
    import marimo as mo
    import plotly as plt
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    return go, make_subplots, mo, np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Preguntas:
    <ul>
        <li>¿Cuál es la tendencia histórica del precio por m² en cada área?</li>
        <li>¿Cuál es la tendencia histórica del precio de venta para cada tipo de registro?</li>
        <li>¿Cuál es la tendencia histórica del precio por m² en cada tipo de propiedad?</li>
        <li>¿Cuál es la tendencia histórica del precio de venta para cada tipo de uso autorizado?</li>
        <li>¿Cuál es la variación porcentual de los últimos 5 años del precio de venta por tipo de registro?</li>
        <li>¿Qué áreas son parte del 80% de las ventas del año 2026?</li>
        <li>¿Cuál es el ranking de áreas que superan la media del precio por m² en 2026?</li>
        <li>¿Cuál es la evolución del volumen de transacciones por año y por tipo de propiedad?</li>
        <li>¿Cuál es el ranking de las 15 áreas con mayor crecimiento del precio por m² en los últimos 5 años?</li>
        <li>¿Cuál es la relación entre tamaño (m²) y precio de venta (o precio/m²) por tipo de propiedad?</li>
        <li>¿Cuál es la distribución del precio por m² por tipo de propiedad en los últimos 3 años?</li>
        <li>Comparación Residencial vs Comercial: precio medio por m² y volumen de transacciones a lo largo del tiempo</li>
    </ul>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Dataframe: Base
    """)
    return


@app.cell(hide_code=True)
def _(mo, np, pd):
    @mo.cache()
    def crear_df_raw():
        df_raw = pd.read_parquet(
            "https://github.com/Gbarrantes25/RealStateDubai-Dashboard/raw/refs/heads/main/dld_sales_transactions.parquet"
        )
        return df_raw

    df_raw = crear_df_raw()

    def crear_df_anos():
        anos = np.arange(1975, 2027)
        dfa = pd.DataFrame(anos, columns=["Fecha_Registro"])
        dfa["Fecha_Registro"] = dfa["Fecha_Registro"].astype(str)
        return dfa

    df_anos = crear_df_anos()

    def crear_df():
        columas_selecccionadas = [
            "transaction_id",
            "instance_date",
            "reg_type_label",
            "property_type_label",
            "area_name_en",
            "property_sub_type",
            "usage_label",
            "area_sqm",
            "price_aed",
            "price_psf",
        ]

        df = df_raw[columas_selecccionadas].copy()
        df["price_psf"] = df["price_psf"].fillna(df["price_aed"] / 10764)
        df = df[df["area_sqm"].notnull()]
        df = df[df["area_name_en"].notnull()]
        df["property_sub_type"] = df["property_sub_type"].fillna("Unknown")
        df = df.reset_index(drop=True)
        df = df.rename(
            columns={
                "transaction_id": "Transacción_Id",
                "instance_date": "Fecha_Registro",
                "reg_type_label": "Tipo_Registro",
                "property_type_label": "Tipo_Propiedad",
                "area_name_en": "Nombre_Area",
                "property_sub_type": "Subtipo_Propiedad",
                "usage_label": "Uso_Autorizado",
                "area_sqm": "m2",
                "price_aed": "Valor_Venta",
                "price_psf": "Precio_m2",
            }
        )
        df["Fecha_Registro"] = pd.to_datetime(
            df["Fecha_Registro"]
        ).dt.to_period("Y")
        df[
            [
                "Tipo_Registro",
                "Tipo_Propiedad",
                "Nombre_Area",
                "Subtipo_Propiedad",
                "Uso_Autorizado",
            ]
        ] = df[
            [
                "Tipo_Registro",
                "Tipo_Propiedad",
                "Nombre_Area",
                "Subtipo_Propiedad",
                "Uso_Autorizado",
            ]
        ].astype("category")

        return df

    df = crear_df()
    df.head(10)
    return df, df_anos


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1. ¿Cuál es la tendencia histórica del precio por m² en cada área?
    """)
    return


@app.cell(hide_code=True)
def _(df, mo):
    areas = sorted(list(df["Nombre_Area"].unique()))
    slicer_area = mo.ui.dropdown(options=areas, value=areas[0], label="Área")
    return (slicer_area,)


@app.cell(hide_code=True)
def _(df, go, slicer_area):
    def crear_tendencia_preciomq_area():

        def crear_df_preciomq_area():
            df_preciomq_area = (
                df[df["Nombre_Area"] == slicer_area.value]
                .groupby("Fecha_Registro")
                .agg({"Precio_m2": "median"})
            ).reset_index()
            df_preciomq_area["Fecha_Registro"] = df_preciomq_area[
                "Fecha_Registro"
            ].astype(str)
            df_preciomq_area["Precio_m2"] = df_preciomq_area[
                "Precio_m2"
            ].round(1)

            return df_preciomq_area

        df_preciomq_area = crear_df_preciomq_area()

        fig = go.Figure()
        lineas = go.Scatter(
            mode="lines+markers",
            line_shape="spline",
            x=df_preciomq_area["Fecha_Registro"],
            y=df_preciomq_area["Precio_m2"],
            name="",
            line={"color": "steelblue"},
            fill="tozeroy",
            fillcolor="lightsteelblue",
            customdata=df_preciomq_area[["Fecha_Registro", "Precio_m2"]],
            hovertemplate="<b>Año: %{customdata[0]}</b><br><b>Precio m²: USD %{customdata[1]}</b>",
        )
        fig.add_traces([lineas])
        fig.update_layout(
            height=400,
            title={
                "text": f"<b>Tendencia histórica del precio por m²: {slicer_area.value}</b>"
            },
        )
        return fig

    return (crear_tendencia_preciomq_area,)


@app.cell(hide_code=True)
def _(crear_tendencia_preciomq_area, mo, slicer_area):
    mo.vstack([slicer_area, crear_tendencia_preciomq_area()])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Hallazgos (ver)": mo.md(
                """
            <ul>
            <li>Jumeirah Second -> 2026 máximo histórico -> USD 8121.42 por encima de la media.</li>
            <li>Um Suqaim First -> 2026 máximo histórico -> USD 5410.53 por encima de la media.</li>
            <li>Ras Al Khor Industrial Third -> 2026 máximo histórico -> USD 3905.88 por encima de la media.</li>
            <li>Al Goze Industrial Third -> 2026 máximo histórico -> USD 3585.11 por encima de la media.</li>
            <li>Al Safouh First -> 2026 máximo histórico -> USD 2847.41 por encima de la media.</li>
            <li>Al Wasl -> 2026 máximo histórico -> USD 2670.65 por encima de la media.</li>
            <li>Jumeirah First -> 2026 máximo histórico -> USD 2619.31 por encima de la media.</li>
            <li>Nad Al Shiba First -> 2026 máximo histórico -> USD 2399.27 por encima de la media.</li>
            <li>Al Karama -> 2026 máximo histórico -> USD 2275.47 por encima de la media.</li>
            <li>Saih Shuaib 1 -> 2026 máximo histórico -> USD 2203.38 por encima de la media.</li>
            </ul>
            """
            )
        },
        expanded=False,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2. ¿Cuál es la tendencia histórica del precio de venta para cada tipo de registro?
    """)
    return


@app.cell(hide_code=True)
def _(df, df_anos, go, pd):
    def crear_tendencia_venta_registro():

        def crear_df_registro(registro: str):
            dfx = (
                (df.loc[df["Tipo_Registro"] == registro])
                .groupby("Fecha_Registro")
                .agg({"Valor_Venta": "sum"})
                .reset_index()
            )
            dfx["Fecha_Registro"] = dfx["Fecha_Registro"].astype(str)
            resultado = dfx.merge(df_anos, how="right", on="Fecha_Registro")
            return resultado

        df_ready = crear_df_registro("Ready")
        df_offplan = crear_df_registro("Off-Plan")

        fig = go.Figure()

        def tendencia(dfx: pd.DataFrame, color: str, nombre: str):
            grafico = go.Scatter(
                x=dfx["Fecha_Registro"],
                y=dfx["Valor_Venta"],
                mode="lines+markers",
                line_shape="spline",
                name=nombre,
                line={"color": color, "dash": "dot"},
                opacity=0.5,
                customdata=dfx[["Fecha_Registro", "Valor_Venta"]],
                hovertemplate="<b>Año: %{customdata[0]}</b><br><b>Venta: USD %{customdata[1]}</b>",
            )
            return grafico

        ready = tendencia(df_offplan, "blue", "Off-Plan")
        offplan = tendencia(df_ready, "red", "Ready")
        fig.add_traces([ready, offplan])
        fig.update_layout(
            title={
                "text": "<b>Tendencia histórica de Precio de Venta por Tipo de Registro</b>"
            },
            height=400,
        )
        return fig

    crear_tendencia_venta_registro()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Hallazgos (ver)": mo.md(
                """
                <ul>
                <li>Históricamente los ingresos por propiedades listas para entregar supera a las de preventas.</li>
                <li>En lo que va del año el valor de venta de los "Ready" y "Off-Plan" van 100B y 180B respectivamente por debajo del 2025. </li>
                </ul>
                """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3. ¿Cuál es la tendencia histórica del precio por m² en cada tipo de propiedad?
    """)
    return


@app.cell(hide_code=True)
def _(df, df_anos, go, pd):
    def crear_tendencia_preciomq_propiedad():

        # ['Villa', 'Land', 'Building', 'Unit']
        def crear_df_tpropiedad(propiedad):
            df_x = (
                df.loc[df["Tipo_Propiedad"] == propiedad]
                .groupby("Fecha_Registro")
                .agg({"Precio_m2": "median"})
                .reset_index()
            )

            df_x["Fecha_Registro"] = df_x["Fecha_Registro"].astype("str")

            df_resultado = df_x.merge(
                df_anos, how="outer", on="Fecha_Registro"
            )
            df_resultado["Fecha_Registro"] = df_resultado[
                "Fecha_Registro"
            ].astype("category")

            return df_resultado

        df_villa = crear_df_tpropiedad("Villa")
        df_land = crear_df_tpropiedad("Land")
        df_building = crear_df_tpropiedad("Building")
        df_unit = crear_df_tpropiedad("Unit")
        fig = go.Figure()

        def crear_linea(dfx: pd.DataFrame, color: str, nombre: str):
            conteo = len(dfx["Precio_m2"])
            dfx["TPropiedad"] = [nombre] * conteo
            grafico = go.Scatter(
                x=dfx["Fecha_Registro"],
                y=dfx["Precio_m2"],
                mode="lines+markers",
                name=nombre,
                line_shape="spline",
                line={"dash": "dot", "color": color},
                opacity=0.5,
                customdata=dfx[["Fecha_Registro", "Precio_m2", "TPropiedad"]],
                hovertemplate="<b>Año: %{customdata[0]}</b><br><b>Precio m²: USD %{customdata[1]:.1f}</b><br><b>T. Propiedad: %{customdata[2]}</b>",
            )
            return grafico

        villa = crear_linea(df_villa, "green", "Villa")
        land = crear_linea(df_land, "steelblue", "Land")
        building = crear_linea(df_building, "orange", "Building")
        unit = crear_linea(df_unit, "red", "Unit")
        fig.add_traces([villa, land, building, unit])
        fig.update_layout(
            title={
                "text": "<b>Tendencia histórica del Precio por m² por tipo de propiedad</b>"
            },
            height=400,
        )
        return fig

    crear_tendencia_preciomq_propiedad()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Hallazgos (ver)": mo.md(
                """
                <ul>
                <li>En los últimos 5 años las propiedades "Villa" y "Building" están creciendo de manera acelerada en el precio por m², mientras que "Land" y "Unit" se mantienen.</li>
                </ul>
                """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4. ¿Cuál es la tendencia histórica del precio de venta para cada tipo de uso autorizado?
    """)
    return


@app.cell(hide_code=True)
def _(df, df_anos, go, pd):
    def crear_tendencia_venta_autorizado():

        # Residential, Commercial, Other
        def crear_df_autorizacion(autorizado: str):

            dfx = (
                df.loc[df["Uso_Autorizado"] == autorizado]
                .groupby("Fecha_Registro")
                .agg({"Valor_Venta": "sum"})
                .reset_index()
            )
            dfx["Fecha_Registro"] = dfx["Fecha_Registro"].astype(str)

            df_resultado = dfx.merge(df_anos, how="outer", on="Fecha_Registro")
            df_resultado["Fecha_Registro"] = df_resultado[
                "Fecha_Registro"
            ].astype("category")
            return df_resultado

        df_residential = crear_df_autorizacion("Residential")
        df_commercial = crear_df_autorizacion("Commercial")
        df_other = crear_df_autorizacion("Other")

        fig = go.Figure()

        def crear_linea(dfx: pd.DataFrame, color: str, nombre: str):
            grafico = go.Scatter(
                x=dfx["Fecha_Registro"],
                y=dfx["Valor_Venta"],
                name=nombre,
                line_shape="spline",
                mode="lines+markers",
                opacity=0.5,
                line={"dash": "dot", "color": color},
                customdata=dfx[["Fecha_Registro", "Valor_Venta"]],
                hovertemplate="<b>Año: %{customdata[0]}</b><br><b>Venta: USD %{customdata[1]}</b>",
            )
            return grafico

        commercial = crear_linea(df_commercial, "steelblue", "Commercial")
        residential = crear_linea(df_residential, "green", "Residential")
        others = crear_linea(df_other, "orange", "Other")
        fig.add_traces([commercial, residential, others])
        fig.update_layout(
            title={
                "text": "<b>Tendencia histórica del precio de Venta por uso autorizado</b>"
            },
            height=400,
        )

        return fig

    crear_tendencia_venta_autorizado()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Hallazgos (ver)": mo.md(
                """
        <ul>
        <li>Si bien el año pasado fue un pico para todas las propiedades de uso autorizado, en lo que va del año se aprecia una caída en todo, en especial en el Residencial.</li>
        <li>Residencial es la categoría que supera entre 100B y 200B a las demás categorías en ventas.</li>
        </ul>
        """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5. ¿Cuál es la variación porcentual de los últimos 5 años del precio de venta por tipo de registro?
    """)
    return


@app.cell(hide_code=True)
def _(df, mo):
    def crear_selector_registro():
        registros = df["Tipo_Registro"].unique()
        selector = mo.ui.dropdown(options=registros, value=registros[0])
        return selector

    selector_registro = crear_selector_registro()
    return (selector_registro,)


@app.cell(hide_code=True)
def _(df, go, np, pd, selector_registro):
    def crear_df_quinquenio():
        ano_min = df["Fecha_Registro"].dt.year.max() - 4
        lista_quinquenio = pd.period_range(
            start=ano_min, periods=5, freq="Y-DEC"
        )
        df_q = pd.DataFrame(lista_quinquenio, columns=["Fecha_Registro"])
        df_q["Fecha_Registro"] = df_q["Fecha_Registro"].astype(str)
        return df_q

    df_quinquenio = crear_df_quinquenio()

    def crear_variacion_venta_quinquenio_registro():
        def crear_df_5anos_registro():

            dfx = (
                df.loc[
                    (
                        df["Fecha_Registro"]
                        >= df_quinquenio["Fecha_Registro"].min()
                    )
                    & (df["Tipo_Registro"] == selector_registro.value)
                ]
                .groupby("Fecha_Registro")
                .agg({"Valor_Venta": "sum"})
            ).reset_index()
            dfx["Fecha_Registro"] = dfx["Fecha_Registro"].astype(str)
            dfx["%YoY"] = dfx["Valor_Venta"].pct_change().round(2)
            df_resultado = dfx.merge(
                df_quinquenio, how="outer", on="Fecha_Registro"
            )

            return df_resultado

        df_grafico = crear_df_5anos_registro()

        nombre = "Ready" if selector_registro.value == "Ready" else "Off-Plan"

        colores_barras = np.where(
            df_grafico["%YoY"] >= 0, "lightsteelblue", "steelblue"
        )
        fig = go.Figure()
        grafico = go.Bar(
            x=df_grafico["Fecha_Registro"],
            y=df_grafico["%YoY"],
            name=nombre,
            marker={"color": colores_barras},
            text=df_grafico["%YoY"],
            texttemplate="<b>%{text}</b>",
            customdata=df_grafico[["Fecha_Registro", "Valor_Venta", "%YoY"]],
            hovertemplate="<b>Año: %{customdata[0]}</b><br><b>%YoY: %{customdata[2]}</b><br><b>Venta Actual: USD %{customdata[1]}</b>",
        )
        fig.add_traces([grafico])
        fig.update_layout(
            title={
                "text": f"<b>Variación % en el Precio de Venta por tipo de registro ({selector_registro.value})</b>"
            },
            height=400,
        )

        return fig

    return crear_variacion_venta_quinquenio_registro, df_quinquenio


@app.cell(hide_code=True)
def _(crear_variacion_venta_quinquenio_registro, mo, selector_registro):
    mo.vstack([selector_registro, crear_variacion_venta_quinquenio_registro()])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Hallazgos (ver)": mo.md(
                """
        <ul>
        <li>En el presente año vemos una caida en las ventas en "Ready" y "Off-Plan" del 49% y 37% respecto al 2025.</li>
        <li>Las propiedades "Ready" hasta el año pasado parecía que se estaba recuperando, pero no fue así. Sin embargo, "Off-Plan" si mantiene su tendencia a la baja en las ventas.</li>
        </ul>
        """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6. ¿Qué áreas son parte del 80% de las ventas del año 2026?
    """)
    return


@app.cell(hide_code=True)
def _(df, mo):
    def crear_selector_anos():
        anos = df["Fecha_Registro"].unique().strftime("%Y")
        selector = mo.ui.dropdown(options=anos, value=anos[-1], label="Años")
        return selector

    selector_anos = crear_selector_anos()
    return (selector_anos,)


@app.cell(hide_code=True)
def _(df, go, selector_anos):
    def crear_pareto_ventas_area():
        def crear_df_pareto_2026():
            df_venta_2026 = (
                df.loc[df["Fecha_Registro"] == selector_anos.value]
                .groupby("Nombre_Area")
                .agg({"Valor_Venta": "sum"})
                .sort_values(by="Valor_Venta", ascending=False)
                .reset_index()
            )
            ventas_totales = df_venta_2026["Valor_Venta"].sum()
            df_venta_2026["%acc"] = (
                ((df_venta_2026["Valor_Venta"] / ventas_totales) * 100)
                .cumsum()
                .round(1)
            )
            df_venta_filtrado = df_venta_2026.loc[df_venta_2026["%acc"] <= 80]
            return df_venta_filtrado

        df_venta_filtrado2026 = crear_df_pareto_2026()

        fig = go.Figure()
        barras = go.Bar(
            x=df_venta_filtrado2026["Nombre_Area"],
            y=df_venta_filtrado2026["Valor_Venta"],
            name="Ventas",
            yaxis="y1",
            marker={"color": "lightsteelblue"},
            customdata=df_venta_filtrado2026[["Nombre_Area", "Valor_Venta"]],
            hovertemplate="<b>Área: %{customdata[0]}</b><br><b>Venta: USD %{customdata[1]}</b>",
        )
        linea = go.Scatter(
            x=df_venta_filtrado2026["Nombre_Area"],
            y=df_venta_filtrado2026["%acc"],
            mode="lines",
            line={"color": "blue", "dash": "dot"},
            yaxis="y2",
            name="%Acc",
            text=df_venta_filtrado2026["%acc"],
            customdata=df_venta_filtrado2026[["Nombre_Area", "%acc"]],
            hovertemplate="<b>Área: %{customdata[0]}</b><br><b>%Acc: %{customdata[1]}%</b>",
        )
        fig.add_traces([barras, linea])
        fig.update_layout(
            yaxis2={"overlaying": "y", "side": "right", "range": [0, 100]},
            title={
                "text": f"<b>Áreas que conforman el 80% de las Ventas del {selector_anos.value}</b>"
            },
        )
        return fig

    return (crear_pareto_ventas_area,)


@app.cell(hide_code=True)
def _(crear_pareto_ventas_area, mo, selector_anos):
    mo.vstack([selector_anos, crear_pareto_ventas_area()])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Hallazgos (ver)": mo.md(
                """
        <ul>
        <li>De las 243 áreas solo el 14% representa el 80% de las ventas en los últimos 5 años.</li>
        </ul>
        """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7. ¿Cuál es el ranking de áreas que superan la media del precio por m² en 2026?
    """)
    return


@app.cell(hide_code=True)
def _(df, mo):
    def crear_selector_anos2():
        anos = df["Fecha_Registro"].unique().strftime("%Y")
        selector = mo.ui.dropdown(options=anos, value=anos[-1], label="Años")
        return selector

    selector_anos2 = crear_selector_anos2()
    return (selector_anos2,)


@app.cell(hide_code=True)
def _(df, mo, selector_anos2):
    def crear_card_mq_media():
        resultado = df.loc[
            df["Fecha_Registro"] == selector_anos2.value,
            "Precio_m2",
        ].median()

        grafico = mo.stat(value=resultado, label="Median", bordered=True)
        return grafico, resultado

    card_precio_media, precio_media = crear_card_mq_media()
    return card_precio_media, precio_media


@app.cell(hide_code=True)
def _(df, go, precio_media, selector_anos2):
    def crear_ranking_precioqm_area():
        def crear_df_grafico():
            dff2 = (
                df.loc[df["Fecha_Registro"] == selector_anos2.value]
                .groupby("Nombre_Area")["Precio_m2"]
                .median()
                .reset_index()
            )

            dff3 = (
                dff2.loc[dff2["Precio_m2"] > precio_media]
                .sort_values(by="Precio_m2", ascending=False)
                .reset_index(drop=True)
            )
            dff3["Precio_m2"] = dff3["Precio_m2"].round(1)

            return dff3

        df_grafico = crear_df_grafico()

        fig = go.Figure()
        grafico = go.Bar(
            x=df_grafico["Nombre_Area"],
            y=df_grafico["Precio_m2"],
            marker={"color": "steelblue"},
            name="",
            customdata=df_grafico[["Nombre_Area", "Precio_m2"]],
            hovertemplate="<b>Área: %{customdata[0]}</b><br><b>Precio por m²: USD %{customdata[1]}</b>",
        )
        fig.add_traces([grafico])
        fig.update_layout(
            title={
                "text": "<b>Ranking de Áreas que superan la media del precio m²</b>"
            }
        )
        return fig

    return (crear_ranking_precioqm_area,)


@app.cell(hide_code=True)
def _(card_precio_media, crear_ranking_precioqm_area, mo, selector_anos2):
    mo.vstack(
        [selector_anos2, card_precio_media, crear_ranking_precioqm_area()],
        heights="equal",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Hallazgos (ver)": """
                 <ul>
                 <li>2026 -> 64 áreas son las que superan la media del precio del m² (USD 1714.84)</li>
                 <li>2025 -> 54 áreas son las que superan la media del precio del m² (USD 1650.47)</li>
                 <li>2024 -> 51 áreas son las que superan la media del precio del m² (USD 1523.21)</li>
                 <li>2023 -> 43 áreas son las que superan la media del precio del m² (USD 1363.15)</li>
                 <li>2022 -> 37 áreas son las que superan la media del precio del m² (USD 1198.06)</li>
                 </ul>
                 """
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8. ¿Cuál es la evolución del volumen de transacciones por año y por tipo de propiedad?
    """)
    return


@app.cell(hide_code=True)
def _(df, df_anos, go, pd):
    def crear_evolucion_transaccion_propiedad():

        def crear_df_transaccion_propiedad(propiedad):
            df_tran = (
                df.loc[df["Tipo_Propiedad"] == propiedad]
                .groupby("Fecha_Registro")
                .agg({"Transacción_Id": "count"})
                .reset_index()
            )
            df_tran["Fecha_Registro"] = df_tran["Fecha_Registro"].astype(str)
            df_resultado = df_tran.merge(
                df_anos, how="outer", on="Fecha_Registro"
            )
            return df_resultado

        df_villa = crear_df_transaccion_propiedad("Villa")
        df_land = crear_df_transaccion_propiedad("Land")
        df_building = crear_df_transaccion_propiedad("Building")
        df_unit = crear_df_transaccion_propiedad("Unit")

        fig = go.Figure()

        def crear_grafico(dfx: pd.DataFrame, color: str, nombre: str):
            grafico = go.Scatter(
                x=dfx["Fecha_Registro"],
                y=dfx["Transacción_Id"],
                name=nombre,
                line_shape="spline",
                mode="lines+markers",
                line={"color": color, "dash": "dot"},
                opacity=0.5,
                customdata=dfx[["Fecha_Registro", "Transacción_Id"]],
                hovertemplate="<b>Año: %{customdata[0]}</b><br><b>Volumen Transacción: %{customdata[1]}</b>",
            )
            return grafico

        villa = crear_grafico(df_villa, "green", "Villa")
        land = crear_grafico(df_land, "steelblue", "Land")
        building = crear_grafico(df_building, "orange", "Building")
        unit = crear_grafico(df_unit, "red", "Unit")
        fig.add_traces([villa, land, building, unit])
        fig.update_layout(
            title={
                "text": "<b>Evolución del Volumen de Transacciones por Tipo de Propiedad</b>"
            },
            height=400,
        )
        return fig

    crear_evolucion_transaccion_propiedad()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Hallazgos (ver)": mo.md(
                """
        <ul>
        <li>Este año se observa una caída en todos los tiempos de propiedad, excepto en "Building" que mantiene su volumen de transacciones.</li>
        <li>Hay una caída en "Unit" de casi el 40% con respecto al año 2025.</li>
        </ul>
        """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 9. ¿Cuál es el ranking de las 15 áreas con mayor crecimiento del precio por m² en los últimos 5 años?
    """)
    return


@app.cell(hide_code=True)
def _(df, df_quinquenio, go):
    def crear_ranking_crecimiento_preciomq():

        ano_min = df_quinquenio["Fecha_Registro"].min()
        ano_max = df_quinquenio["Fecha_Registro"].max()

        def crear_df_anos_filtrados():
            anos_lista = [ano_min, ano_max]
            df_filtro = df.loc[
                df["Fecha_Registro"].dt.year.astype(str).isin(anos_lista)
            ].copy()
            df_pivot = df_filtro.pivot_table(
                values="Precio_m2",
                index="Nombre_Area",
                columns="Fecha_Registro",
                aggfunc="median",
            )
            df_pivot.columns = df_pivot.columns.astype(str)
            df_resultado = df_pivot.loc[df_pivot[ano_min] > 0].copy()
            df_resultado["%Crecimiento"] = (
                (df_resultado[ano_max] - df_resultado[ano_min])
                / df_resultado[ano_min]
            ).round(1) * 100
            df_resultado = df_resultado.sort_values(
                by="%Crecimiento", ascending=False
            ).reset_index()

            return df_resultado.head(15)

        df_anos_crecimiento = crear_df_anos_filtrados()

        fig = go.Figure()
        ranking = go.Bar(
            x=df_anos_crecimiento["%Crecimiento"],
            y=df_anos_crecimiento["Nombre_Area"],
            orientation="h",
            marker={"color": "steelblue"},
            customdata=df_anos_crecimiento[
                ["Nombre_Area", "%Crecimiento", ano_min, ano_max]
            ],
            hovertemplate="<b>Área: %{customdata[0]}</b><br><b>%Crecimiento: %{customdata[1]}%</b><br><b>Año Inicial (Precio m²): USD %{customdata[2]:.1f}</b><br><b>último Año (Precio m²): USD %{customdata[3]:.1f}</b>",
        )
        fig.add_traces([ranking])
        fig.update_layout(
            title={
                "text": "<b>Ranking de Áreas con mayor crecimiento del Precio del m² de los últimos 5 años</b>"
            },
            yaxis={"autorange": "reversed"},
        )
        return fig

    crear_ranking_crecimiento_preciomq()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Hallazgos (ver)": mo.md(
                """
        <ul>
        <li>Todos las áreas de este ranking (como mínimo) han tripicado el Precio del m² en los últimos 5 años.</li>
        </ul>
        """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 10. ¿Cuál es la relación entre tamaño (m²) y precio de venta (o precio/m²) por tipo de propiedad?
    """)
    return


@app.cell(hide_code=True)
def _(df, go, make_subplots):
    def crear_hetmap_propiedad():
        def crear_df_heatmap_propiedad(propiedad):
            df_resultado = df.loc[
                df["Tipo_Propiedad"] == propiedad,
                ["Precio_m2", "m2", "Valor_Venta"],
            ]

            return df_resultado

        df_villa = crear_df_heatmap_propiedad("Villa").corr()
        df_land = crear_df_heatmap_propiedad("Land").corr()
        df_building = crear_df_heatmap_propiedad("Building").corr()
        df_unit = crear_df_heatmap_propiedad("Unit").corr()

        fig = make_subplots(
            cols=2,
            rows=2,
            subplot_titles=("Villa", "Land", "Building", "Unit"),
        )
        fig.add_trace(
            go.Heatmap(
                z=df_villa.values,
                x=df_villa.columns,
                y=df_villa.index,
                coloraxis="coloraxis",
                name="",
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Heatmap(
                z=df_land.values,
                x=df_land.columns,
                y=df_land.index,
                coloraxis="coloraxis",
                name="",
            ),
            row=1,
            col=2,
        )
        fig.add_trace(
            go.Heatmap(
                z=df_building.values,
                x=df_building.columns,
                y=df_building.index,
                coloraxis="coloraxis",
                name="",
            ),
            row=2,
            col=1,
        )
        fig.add_trace(
            go.Heatmap(
                z=df_unit.values,
                x=df_unit.columns,
                y=df_unit.index,
                coloraxis="coloraxis",
                name="",
            ),
            row=2,
            col=2,
        )

        fig.update_layout(
            title={
                "text": "<b>Matrices de Correlación por Tipo de Propiedad</b>"
            },
            height=580,
            coloraxis=dict(
                colorscale=["#e3f2fd", "#90caf9", "#0d47a1"],
                cmin=-1,
                cmax=1,
                colorbar=dict(thickness=20),
            ),
        )
        return fig

    crear_hetmap_propiedad()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Hallazgos (ver)": mo.md(
                """
        <ul>
        <li>Villa -> La venta está moderadamente correlacionada con el precio del m².</li>
        <li>Land -> Sus correlaciones son débiles.</li>
        <li>Building -> La venta está moderadamente correlacionada con el precio del m². El m² es una correlación inversa al precio del m².</li>
        <li>Unit -> La venta está moderadamente correlacionada con el precio del m² y lo mismo el m² con la venta.</li>
        </ul>
        """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 11. ¿Cuál es la distribución del precio por m² por tipo de propiedade en los últimos 3 años?
    """)
    return


@app.cell(hide_code=True)
def _(df, df_anos, go, make_subplots, np, pd):
    def crear_distribucion_histograma_propiedad():
        ano3 = str(
            int(pd.to_datetime(df_anos["Fecha_Registro"]).dt.year.max() - 2)
        )

        def crear_df_histogram(propiedad):
            dfx = df.loc[
                (df["Tipo_Propiedad"] == propiedad)
                & (df["Fecha_Registro"] >= ano3)
            ].reset_index()
            qbajo = dfx["Precio_m2"].quantile(0.01)
            qalto = dfx["Precio_m2"].quantile(0.99)
            df_resultado = dfx.loc[
                (dfx["Precio_m2"] >= qbajo) & (dfx["Precio_m2"] <= qalto)
            ]["Precio_m2"].reset_index(drop=True)

            return df_resultado

        df_villa = crear_df_histogram("Villa")
        df_land = crear_df_histogram("Land")
        df_building = crear_df_histogram("Building")
        df_unit = crear_df_histogram("Unit")

        fig = make_subplots(
            cols=2,
            rows=2,
            subplot_titles=["Villa", "Land", "Building", "Unit"],
        )

        def crear_histograma(
            dfx: pd.DataFrame, color: str, nombre: str, fila: int, col: int
        ):
            start_m2 = np.floor(dfx.min())
            end_m2 = np.ceil(dfx.max())
            size_m2 = (end_m2 - start_m2) / 5
            grafico = fig.add_trace(
                go.Histogram(
                    x=dfx,
                    xbins={"start": start_m2, "end": end_m2, "size": size_m2},
                    marker={"color": color},
                    name=nombre,
                    autobinx=False,
                ),
                row=fila,
                col=col,
            )
            return grafico

        crear_histograma(df_villa, "steelblue", "Villa", 1, 1)
        (crear_histograma(df_land, "royalblue", "Land", 1, 2),)
        (crear_histograma(df_building, "dodgerblue", "Building", 2, 1),)
        (crear_histograma(df_unit, "mediumblue", "Unit", 2, 2),)

        fig.update_layout(
            title={
                "text": "<b>Distribución del Premio del m² por Tipo de Propiedad en los últimos 3 años</b>"
            }
        )
        return fig

    crear_distribucion_histograma_propiedad()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Hallazgos (ver)": mo.md(
                """
        <ul>
        <li>El precio del m² en todos los tipos de propiedad se intensifican en el grupo 2.</li>
        <li>Solo "Unit" tiene cierto volumen de datos en el grupo 1.</li>
        </ul>
        """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 12. Comparación Residencial vs Comercial: precio medio por m² y volumen de transacciones a lo largo del tiempo
    """)
    return


@app.cell(hide_code=True)
def _(df, df_anos, go, pd):
    def crear_historico_comparativo():
        def crear_df_autorizado(autorizado: str):
            df_r = (
                df.loc[
                    df["Uso_Autorizado"] == autorizado,
                    ["Transacción_Id", "Fecha_Registro", "Precio_m2"],
                ]
                .groupby("Fecha_Registro")
                .agg({"Precio_m2": "median", "Transacción_Id": "count"})
                .reset_index()
            )
            df_r["Fecha_Registro"] = df_r["Fecha_Registro"].astype(str)
            df_resultado = df_r.merge(
                df_anos, how="outer", on="Fecha_Registro"
            )
            df_resultado["Precio_m2"] = df_resultado["Precio_m2"].round(1)
            return df_resultado

        df_residencial = crear_df_autorizado("Residential")
        df_comercial = crear_df_autorizado("Commercial")

        def crear_scatter_historico_autorizado():
            fig = go.Figure()

            def crear_grafico(dfx: pd.DataFrame, color: str, nombre: str):
                scatter = go.Scatter(
                    x=dfx["Fecha_Registro"],
                    y=dfx["Precio_m2"],
                    name=nombre,
                    marker={"color": color, "size": 12},
                    mode="markers",
                    opacity=0.8,
                    customdata=dfx[["Fecha_Registro", "Precio_m2"]],
                    hovertemplate="<b>Año: %{customdata[0]}</b><br><b>Precio m²: USD %{customdata[1]}</b>",
                )
                return scatter

            residencial = crear_grafico(
                df_residencial, "steelblue", "Residential"
            )
            comercial = crear_grafico(
                df_comercial, "lightskyblue", "Commercial"
            )

            fig.add_traces([residencial, comercial])
            fig.update_layout(
                title={
                    "text": "<b>Histórico Precio m²: Residencial vs Comercial</b>"
                },
                height=400,
            )
            return fig

        def crear_linea_historico_autorizado():
            fig = go.Figure()

            def crear_grafico(dfx: pd.DataFrame, color: str, nombre: str):
                linea = go.Scatter(
                    x=dfx["Fecha_Registro"],
                    y=dfx["Transacción_Id"],
                    name=nombre,
                    marker={"color": color, "size": 12},
                    line={"dash": "dot"},
                    mode="markers",
                    opacity=0.8,
                    customdata=dfx[["Fecha_Registro", "Transacción_Id"]],
                    hovertemplate="<b>Año: %{customdata[0]}</b><br><b>Volumen Transacción: %{customdata[1]}</b>",
                    line_shape="spline",
                )
                return linea

            residencial = crear_grafico(
                df_residencial, "steelblue", "Residential"
            )
            comercial = crear_grafico(
                df_comercial, "lightskyblue", "Commercial"
            )

            fig.add_traces([residencial, comercial])
            fig.update_layout(
                title={
                    "text": "<b>Histórico Volumen Transaccional: Residencial vs Comercial</b>"
                },
                height=400,
            )
            return fig

        scatter_hist = crear_scatter_historico_autorizado()
        linea_hist = crear_linea_historico_autorizado()
        return scatter_hist, linea_hist

    scatter_hist, linea_hist = crear_historico_comparativo()
    return linea_hist, scatter_hist


@app.cell(hide_code=True)
def _(linea_hist, mo, scatter_hist):
    mo.vstack([scatter_hist, linea_hist])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Hallazgos (ver)": mo.md(
                """
        <ul>
        <li>En los últimos dos años el preico por m² entre los inmuebles comerciales y residenciales se están equiparando como en el 2014-2015.</li>
        <li>El volumen transaccional de las propiedades comerciales se mantiene, mientras que las residenciales caen en 80k respecto al año 2025. La tendencia de las propiedades residenciales suelen ser más volátiles como se visualiza en el gráfico.</li>
        </ul>
        """
            )
        }
    )
    return


if __name__ == "__main__":
    app.run()
