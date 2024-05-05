import streamlit as st
import pandas as pd
import math as math
from handcalcs.decorator import handcalc
import forallpeople as si
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
 
si.environment("structural")

st.write("##### DESIGN AND DETAILING OF REINFORCED CONCRETE WALLS TO AS 3600:2018")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Overview",
                                            "Etabs pier output and design parameters", 
                                            "Wall Stresses","Simplified wall design",
                                            "Design as column",
                                            "Need Help or Want to Contribute?"])

with tab1:
    st.markdown("<p style='color:red;'>Introduction</p>", unsafe_allow_html=True)
    st.markdown("This web-based application is designed to analyze ETABS pier output and to design reinforced concrete walls in accordance with AS3600:2018 to resist wind, earthquake and gravity actions.")
                
    st.markdown("The manual execution of this design procedure can be onerous but leveraging the power of Python programming, this process have been streamlined and the workflow optimized to a reasonable extent thereby enhancing the efficiency of the design.")
    st.markdown("<p style='color:red;'>Design assumptions and limitations</p>", unsafe_allow_html=True)

    st.markdown("* This application assumes all walls are doubly reinforced, design of singly reinforced wall sections are outside the scope of this software.")
    st.markdown("* In cases where the wall aligns with the criteria specified in cl11.2.1(b) of AS 3600:2018 and necessitates a strut-and-tie design, the design engineer must assess whether the loading and support conditions justify a non-flexural analysis, and proceed with the design accordingly, this is outside the scope of this application.")
    st.markdown("* All walls are assumed to be braced and in determining the effective height of the walls, one-way buckling and a k-factor of 1 have been adopted.")
    st.markdown("* This application is not a substitute for critical thinking and professional judgement. Users should independently review and validate the results obtained and, when in doubt, seek guidance of experienced engineers. ")
    st.markdown("* Slender walls will be addressed in future updates.")
try:
    with tab2:
        Ductility_factor = st.selectbox("Select Ductility factor (μ):", options=('1','2','3'))
        if Ductility_factor=='1':
            uploaded_file = st.file_uploader("ETABS Pier forces:", type=["xlsx"])
            if uploaded_file is not None:
                st.markdown("""<style>label[for="uploadFile"] {color: red !important;}</style>""",unsafe_allow_html=True)
                df_forces = pd.read_excel(uploaded_file)

            uploaded_file = st.file_uploader("ETABS Pier properties:", type=["xlsx"])
            if uploaded_file is not None:
                df_pier_props = pd.read_excel(uploaded_file)

            uploaded_file = st.file_uploader("ETABS storey heights:", type=["xlsx"])
            if uploaded_file is not None:
                df_storey_heights = pd.read_excel(uploaded_file)
            Sturctural_performance_factor = st.selectbox("Sturctural performance factor (Sp):", options=('0.67','0.77','1'))
            Soil_classification = st.selectbox("Site soil classification:", options=('Ae - Strong rock','Be - Rock','Ce - Shallow soil', 'De - Deep or soft soil', 'Ee - Very soft soil'))

            df_forces2 = df_forces.drop([0], axis=0)
            st.markdown("ETABS Pier Forces")
            st.dataframe(df_forces2)
            mask=df_forces2['Case Type'] == 'Combination'
            df_combos = df_forces2.loc[mask]
            st.markdown("Combination Load Cases")
            st.dataframe(df_combos)

            #MAX TENSION IN PIERS CHECK
            mask = df_combos['P'] > 0
            p_tens = df_combos.loc[mask]
            p_tens['P'] = pd.to_numeric(p_tens['P'], errors='coerce')
            p_tens_loc = p_tens.groupby(["Story","Pier"])["P"].groups
            p_tens_idxmax = p_tens.groupby(["Story","Pier"])["P"].idxmax()
            p_tens_max = p_tens.loc[p_tens_idxmax]
            #st.dataframe(p_tens_max)
            p_tens_max = p_tens_max.set_index("Story")

            #st.dataframe(df_storey_heights)
            df_story_height = df_storey_heights.drop([0], axis=0)
            df_story_height2 = df_story_height.drop(['Master Story',
                                                    'Similar To',
                                                    'Splice Story',
                                                    'Splice Height',
                                                    'Color','GUID'], axis=1)
            #st.dataframe(df_story_height2)

            df_story=df_story_height2
            Story_list = df_story['Name'].tolist()
            stories = Story_list[:-1]

            story_categorical = pd.CategoricalDtype(stories, ordered=True)
            p_tens_max.index = p_tens_max.index.astype(story_categorical)
            p_tens_dtype = p_tens_max.sort_index()
            #st.dataframe(p_tens_dtype)

            #MIN COMPRESSION IN PIERS CHECK
            mask = df_combos['P'] < 0
            p_tens_min_compr = df_combos.loc[mask]
            p_tens_min_compr['P'] = pd.to_numeric(p_tens_min_compr['P'], errors='coerce')
            min_compr_tens = p_tens_min_compr.groupby(["Story","Pier"])["P"].max().reset_index()
            min_compr_tens_idxmax = p_tens_min_compr.groupby(["Story","Pier"])["P"].idxmax()
            p_tens_max2 = p_tens_min_compr.loc[min_compr_tens_idxmax]

            #df_story=df_story_height2
            #Story_list = df_story['Name'].tolist()
            #stories = Story_list[:-1]

            story_categorical = pd.CategoricalDtype(stories, ordered=True)
            p_tens_max2.index = p_tens_max2.index.astype(story_categorical)
            p_tens2_dtype = p_tens_max2.sort_index()
            #st.dataframe(p_tens2_dtype)

            #MAX COMPRESSION IN PIERS CHECK
            mask = df_combos['P'] < 0
            p_compr = df_combos.loc[mask]
            p_compr['P'] = pd.to_numeric(p_compr['P'], errors='coerce')
            p_compr_loc = p_compr.groupby(["Story","Pier"])["P"].groups
            p_compr_idxmax = p_compr.groupby(["Story","Pier"])["P"].idxmin()
            p_compr_max = p_compr.loc[p_compr_idxmax]
            #st.dataframe(p_compr_max)
            p_compr_max = p_compr_max.set_index("Story")

            #st.dataframe(df_storey_heights)
            df_story_height = df_storey_heights.drop([0], axis=0)
            df_story_height2 = df_story_height.drop(['Master Story',
                                                    'Similar To',
                                                    'Splice Story',
                                                    'Splice Height',
                                                    'Color','GUID'], axis=1)
            #st.dataframe(df_story_height2)

            df_story=df_story_height2
            Story_list = df_story['Name'].tolist()
            stories = Story_list[:-1]

            story_categorical = pd.CategoricalDtype(stories, ordered=True)
            p_compr_max.index = p_compr_max.index.astype(story_categorical)
            p_compr_dtype = p_compr_max.sort_index()
            #st.dataframe(p_compr_dtype)

            #MAX M3 IN PIERS CHECK
            df_combos['M3'] = pd.to_numeric(df_combos['M3'], errors='coerce')
            m3_loc = df_combos.groupby(["Story","Pier"])["M3"].groups
            m3_idxmax = df_combos.groupby(["Story","Pier"])["M3"].apply(lambda x: x.abs().idxmax())
            m3_max = df_combos.loc[m3_idxmax]
            m3_max = m3_max.set_index("Story")
            m3_max.index = m3_max.index.astype(story_categorical)
            m3_dtype = m3_max.sort_index()
            #st.dataframe(m3_dtype)

            #MAX V2 IN PIERS CHECK
            df_combos['V2'] = pd.to_numeric(df_combos['V2'], errors='coerce')
            v2_loc = df_combos.groupby(["Story","Pier"])["V2"].groups
            v2_idxmax = df_combos.groupby(["Story","Pier"])["V2"].apply(lambda x: x.abs().idxmax())
            v2_max = df_combos.loc[v2_idxmax]
            v2_max = v2_max.set_index("Story")
            v2_max.index = v2_max.index.astype(story_categorical)
            v2_dtype = v2_max.sort_index()
            #st.dataframe(v2_dtype)

            #MERGE DATAFRAMES
            p_tens_ = p_tens_dtype.drop(["Case Type","Step Type","Location"], axis=1)
            p_compr_ = p_compr_dtype.drop(["Case Type","Step Type","Location"], axis=1)
            m3_ = m3_dtype.drop(["Case Type","Step Type","Location"], axis=1)
            v2_ = v2_dtype.drop(["Case Type","Step Type","Location"], axis=1)
            tens_compr_merge = p_compr_.merge(p_tens_,on=["Story","Pier"],how='outer')
            tens_compr_merge.index = tens_compr_merge.index.astype(story_categorical)
            p_t_merged = tens_compr_merge.sort_index()

            p_t_m3 = p_t_merged.merge(m3_,on=["Story","Pier"],how='outer')
            #st.dataframe(p_t_merged)

            p_t_m3_v2 = p_t_m3.merge(v2_,on=["Story","Pier"],how='outer', suffixes=('_x1','_y1'))
            df_combined = p_t_m3_v2
            #st.dataframe(df_combined)

            ##Story heights
            story_prop=df_story_height2
            story_properties = story_prop.iloc[:-1]
            story_prop3=story_properties.rename(columns={"Name":"Story"})
            story_prop4=story_prop3.set_index("Story")
            #st.dataframe(story_prop4)
            df_combined2 = df_combined.merge(story_prop4,on=["Story"],how='outer')
            #st.dataframe(df_combined2)

            ##Sort index
            #st.dataframe(df_pier_props)
            df_pier_prop = df_pier_props.drop([0], axis=0)
            pier_props = df_pier_prop.drop(['AxisAngle',
                                            '# Area Objects',
                                            '# Line Objects',
                                            'Width Top',
                                            'Thickness Top',
                                            'Material',
                                            'CG Bottom X',
                                            'CG Bottom Y',
                                            'CG Bottom Z',
                                            'CG Top X',
                                            'CG Top Y',
                                            'CG Top Z'], axis=1)
            pier_props1=pier_props.set_index("Story")
            df_combined3 = df_combined2.merge(pier_props,on=["Story","Pier"],how='outer')
            #st.dataframe(df_combined3)

            df_combined3.index = df_combined3.index.astype(story_categorical)
            walls_df = df_combined3.sort_index()
            walls_df2 = walls_df.set_index('Story')
            #st.dataframe(walls_df2)
            pier_forces_cleaned=walls_df2.fillna(0)
            #st.dataframe(pier_forces_cleaned)
            mu1_pier_forces = pier_forces_cleaned.drop(['Step Number_x',
                                                        'Step Label_x',
                                                        'Step Number_y',
                                                        'Step Label_y',
                                                        'Step Number_x1',
                                                        'Step Label_x1',
                                                        'Step Number_y1',
                                                        'Step Label_y1',
                                                        'T_x',
                                                        'T_y',
                                                        'T_x1',
                                                        'T_y1'],axis=1)
            #st.dataframe(mu1_pier_forces)
            mu1_pier_forces.columns=['Pier',
                                    'Output Case(Compr)',
                                    'P(Compr)',
                                    'V2(Compr)',
                                    'V3(Compr)',
                                    'M2(Compr)',
                                    'M3(Compr)',
                                    'Output Case(Tens)',
                                    'P(Tens)',
                                    'V2(Tens)',
                                    'V3(Tens)',
                                    'M2(Tens)',
                                    'M3(Tens)',
                                    'Output Case(Max M3)',
                                    'P(Max M3)',
                                    'V2(Max M3)',
                                    'V3(Max M3)',
                                    'M2(Max M3)',
                                    'M3(Max M3)',
                                    'Output Case(Max V2)',
                                    'P(Max V2)',
                                    'V2(Max V2)',
                                    'V3(Max V2)',
                                    'M2(Max V2)',
                                    'M3(Max V2)',
                                    'H',
                                    'd',
                                    'b']
            st.markdown("Maximum forces in Piers")
            st.dataframe(mu1_pier_forces)


            #Multiindex columns
            #mu1_columns=pd.MultiIndex.from_tuples([('','Pier'),
            #                                     ('Maximum Compression Case','Output Case(Compr)'),
            #                                     ('Maximum Compression Case','P(Compr)'),
            #                                     ('Maximum Compression Case','V2(Compr)'),
            #                                    ('Maximum Compression Case','V3(Compr)'),
            #                                     ('Maximum Compression Case','M2(Compr)'),
            #                                     ('Maximum Compression Case','M3(Compr)'),
            #                                     ('Maximum Tension or Minimum Compression Case','Output Case(Tens)'),
            #                                     ('Maximum Tension or Minimum Compression Case','P(Tens)'),
            #                                     ('Maximum Tension or Minimum Compression Case','V2(Tens)'),
            #                                     ('Maximum Tension or Minimum Compression Case','V3(Tens)'),
            #                                     ('Maximum Tension or Minimum Compression Case','M2(Tens)'),
            #                                     ('Maximum Tension or Minimum Compression Case','M3(Tens)'),
            #                                     ('Maximum M3 Case','Output Case(Max M3)'),
            #                                     ('Maximum M3 Case','P(Max M3)'),
            #                                     ('Maximum M3 Case','V2(Max M3)'),
            #                                     ('Maximum M3 Case','V3(Max M3)'),
            #                                    ('Maximum M3 Case','M2(Max M3)'),
            #                                     ('Maximum M3 Case','M3(Max M3)'),
            #                                     ('Maximum V2 Case','Output Case(Max V2)'),
            #                                     ('Maximum V2 Case','P(Max V2)'),
            #                                     ('Maximum V2 Case','V2(Max V2)'),
            #                                     ('Maximum V2 Case','V3(Max V2)'),
            #                                     ('Maximum V2 Case','M2(Max V2)'),
            #                                     ('Maximum V2 Case','M3(Max V2)'),
            #                                     ('','H'),
            #                                     ('','d'),
            #                                     ('','b')])
            #mu1_forces = pd.DataFrame(mu1_pier_forces,columns=mu1_columns)
            #st.table(mu1_forces)

        with tab3:
            df=mu1_pier_forces
            def second_moment_area(row: pd.Series) -> float:
                """
                Returns the second moment of area of the concrete section(I), unit: mm**4
                """
                d = row["d"] # length of the wall
                b = row["b"] # width of the wall
                I = (b*(d**3))/12
                return I   
            df["I"] = df.apply(second_moment_area, axis=1)


            def depth_of_neutral_axis(row: pd.Series) -> float:
                """
                Returns the distance between the extreme stress fibre to centroid of the wall (y), unit: mm
                """
                d = row["d"] # length of the wall
                y = d/2
                return y   
            df["y"] = df.apply(depth_of_neutral_axis, axis=1)

            def section_modulus(row: pd.Series) -> float:
                """
                Returns the section modulus of the wall section, unit: mm**3
                """
                I = row["I"]
                y = row["y"]
                Z = I/y
                return Z   
            df["Z"] = df.apply(section_modulus, axis=1)

            def bending_stress_compression(row: pd.Series) -> float:
                """
                Returns the bending stress due to maximum axial forces(compression), unit: mpa
                """
                M = abs(row["M3(Compr)"]*10**6)
                Z = row["Z"]
                bending_stress_compr = M/Z
                return bending_stress_compr
            df["bending_stress_compr"] = df.apply(bending_stress_compression, axis=1)

            def axial_stress_compression(row: pd.Series) -> float:
                """
                Returns the axial stress due to maximum axial forces(compression), unit: mpa
                """
                P = row["P(Compr)"]*10**3
                A = row["b"]*row["d"]
                axial_stress_compr = P/A
                return axial_stress_compr
            df["axial_stress_compr"] = df.apply(axial_stress_compression, axis=1)

            def bending_stress_tension(row: pd.Series) -> float:
                """
                Returns the bending stress due to minimum axial forces (compression or tension), unit: mpa
                """
                M = abs(row["M3(Tens)"]*10**6)
                Z = row["Z"]
                bending_stress_tens = M/Z
                return bending_stress_tens
            df["bending_stress_tens"] = df.apply(bending_stress_tension, axis=1)

            def axial_stress_tension(row: pd.Series) -> float:
                """
                Returns the axial stress due to minimum axial forces (compression or tension), unit: mpa
                """
                P = row["P(Tens)"]*10**3
                A = row["b"]*row["d"]
                axial_stress_tens = P/A
                return axial_stress_tens
            df["axial_stress_tens"] = df.apply(axial_stress_tension, axis=1)

            def bending_stress_m3(row: pd.Series) -> float:
                """
                Returns the bending stress due to max M3 forces, unit: mpa
                """
                M = abs(row["M3(Max M3)"]*10**6)
                Z = row["Z"]
                bending_stress_m3 = M/Z
                return bending_stress_m3
            df["bending_stress_m3"] = df.apply(bending_stress_m3, axis=1)

            def axial_stress_m3(row: pd.Series) -> float:
                """
                Returns the axial stress due to max m3 forces, unit: mpa
                """
                P = row["P(Max M3)"]*10**3
                A = row["b"]*row["d"]
                axial_stress_m3 = P/A
                return axial_stress_m3
            df["axial_stress_m3"] = df.apply(axial_stress_m3, axis=1)

            def max_stresses_compr(row: pd.Series) -> float:
                """
                Returns the maximum compression stresses in the section under maximum axial forces, unit: mpa
                """
                bending_stress = row["bending_stress_compr"]
                axial_stress = row["axial_stress_compr"]
                max_compr = abs(axial_stress) + bending_stress
                return max_compr
            df["Compr_stresses(max_P_case)"] = df.apply(max_stresses_compr, axis=1)

            def max_stresses_tens(row: pd.Series) -> float:
                """
                Returns the maximum tension stresses in the section under maximum axial forces, unit: mpa
                """
                bending_stress = row["bending_stress_compr"]
                axial_stress = row["axial_stress_compr"]
                max_tens = bending_stress-abs(axial_stress)
                no_tens = 0
                if max_tens > 0:
                    return max_tens
                else:
                    return no_tens
            df["tens_stresses(max_P_case)"] = df.apply(max_stresses_tens, axis=1)

            def max_stresses_compr(row: pd.Series) -> float:
                """
                Returns the maximum compression in the section under minimum axial forces, unit: mpa
                """
                bending_stress = row["bending_stress_tens"]
                axial_stress = row["axial_stress_tens"]
                if axial_stress > 0:
                    max_compr = bending_stress - abs(axial_stress)
                elif axial_stress < 0:
                    max_compr = bending_stress + abs(axial_stress)
                elif axial_stress == 0:
                    max_compr = 0
                return max_compr
            df["Compr_stresses(max_tens_case)"] = df.apply(max_stresses_compr, axis=1)

            def max_stresses_tens(row: pd.Series) -> float:
                """
                Returns the maximum tension stresses in the section under minimum axial forces, unit: mpa
                """
                bending_stress = row["bending_stress_tens"]
                axial_stress = row["axial_stress_tens"]
                if axial_stress > 0:
                    max_tens = bending_stress + abs(axial_stress)
                elif axial_stress < 0:
                    max_tens = bending_stress - abs(axial_stress)
                elif axial_stress == 0:
                    max_tens = 0
                return max_tens
            df["tens_stresses(max_tens_case)"] = df.apply(max_stresses_tens, axis=1)

            def max_stresses_compr2(row: pd.Series) -> float:
                """
                Returns the maximum compression stresses in the section under maximum bending moments, unit: mpa
                """
                bending_stress = row["bending_stress_m3"]
                axial_stress = row["axial_stress_m3"]
                if axial_stress > 0:
                    max_compr = bending_stress - abs(axial_stress)
                elif axial_stress < 0:
                    max_compr = bending_stress + abs(axial_stress)
                elif axial_stress == 0:
                    max_compr = 0
                return max_compr
            df["Compr_stresses(max_m3_case)"] = df.apply(max_stresses_compr2, axis=1)

            def max_stresses_tens2(row: pd.Series) -> float:
                """
                Returns the maximum tensile stresses in the section under maximum bending moments, unit: mpa
                """
                bending_stress = row["bending_stress_m3"]
                axial_stress = row["axial_stress_m3"]
                if axial_stress > 0:
                    max_tens = bending_stress + abs(axial_stress)
                elif axial_stress < 0:
                    max_tens = bending_stress - abs(axial_stress)
                elif axial_stress == 0:
                    max_tens = 0
                return max_tens
            df["tens_stresses(max_m3_case)"] = df.apply(max_stresses_tens2, axis=1)

            #def net_compr_stress(row: pd.Series) -> float:
                #"""
                #Returns the maximum compressive stress in the section, unit: mpa
                #"""
            # #p_compr = row["Compr_stresses(max_P_case)"]
                #t_compr = row["Compr_stresses(max_tens_case)"]
                #m3_compr = row["Compr_stresses(max_m3_case)"]
                #p_tens = row["tens_stresses(max_P_case)"]
                #t_tens = row["tens_stresses(max_tens_case)"]
                #m3_tens = row["tens_stresses(max_m3_case)"]
                
                #if t_compr > 0:
                    #net_compression = max(p_compr,t_compr,m3_compr)
                #else:
                    #t_compr <= 0
                    #net_compression = max(p_compr,m3_compr)
                #return net_compression
            #f["Net compression stress"] = df.apply(net_compr_stress, axis=1)

            def net_compr_stress(row: pd.Series) -> float:
                """
                Returns the maximum compressive stress in the section, unit: mpa
                """
                p_compr = row["Compr_stresses(max_P_case)"]
                t_compr = row["Compr_stresses(max_tens_case)"]
                m3_compr = row["Compr_stresses(max_m3_case)"]
                net_compression = max(p_compr,t_compr,m3_compr)
                return net_compression
            df["Net compression stress"] = df.apply(net_compr_stress, axis=1)

            def net_tens_stress(row: pd.Series) -> float:
                """
                Returns the maximum compressive stress in the section, unit: mpa
                """
                p_tens = row["tens_stresses(max_P_case)"]
                t_tens = row["tens_stresses(max_tens_case)"]
                m3_tens = row["tens_stresses(max_m3_case)"]
                net_tens = max(p_tens,t_tens,m3_tens)
                return net_tens
            df["Net tension stress"] = df.apply(net_tens_stress, axis=1)
                #if t_tens > 0:
                    #net_tens = max((min(p_tens,m3_tens)),t_tens)
                    #return net_tens
                #if t_tens <= 0:
                    #net_tens = min(p_tens,m3_tens)
                    #return net_tens
                #if t_tens == 0 and min(p_tens,m3_tens) > 0:
                    #net_tens = 0
                    #return net_tens
            #df["Net tension stress"] = df.apply(net_tens_stress, axis=1)
            st.markdown("**Calculated stresses in all walls**")
            st.dataframe(df)    
            df2 = df
            df2['Net tension stress'] = pd.to_numeric(df2['Net tension stress'], errors='coerce')
            mask = df2['Net tension stress'] != 0
            design_col = df2.loc[mask]
            st.markdown("**Walls to be designed as columns**")
            st.dataframe(design_col)
            #df2
            #df2['Net tension stress'] = pd.to_numeric(df2['Net tension stress'], errors='coerce')
            mask = df2['Net tension stress'] == 0.000000
            design_wall = df2.loc[mask]
            st.markdown("**Walls to be designed using simplified method**")
            st.dataframe(design_wall)

        with tab4:
            #Soil_classification = st.selectbox("Site soil classification:", options=('Ae - Strong rock','Be - Rock','Ce - Shallow soil', 'De - Deep or soft soil', 'Ee - Very soft soil'))
            if Soil_classification == "De - Deep or soft soil" or Soil_classification == "Ee - Very soft soil""Ee - Very soft soil":
                st.markdown("Simplified design method for compression forces does not apply (CL11.5.2(c)), design all walls as columns as per Section 10.")
            else:
                df=design_wall
                df.set_index(['Pier',df.index], inplace=True)
                st.markdown("Walls with no tensile stresses")
                st.dataframe(df)
                #df2=df.index
                #st.dataframe(df2)
                unique_stories = df.index.get_level_values('Pier').unique()
                selected_story = st.selectbox("Select a Pier:", unique_stories)
                unique_piers = df.index.get_level_values('Story').unique()
                selected_pier = st.selectbox("Select a Story:", unique_piers)

                col1, col2 = st.columns([1,2])
                with col2:
                    try:
                        Pier_forces = df.loc[(selected_story, selected_pier)]
                        st.write("Selected Pier forces:")
                        st.write(Pier_forces)
                    except KeyError:
                        st.write("Selected story and pier combination is not available.")

                with col1:
                    st.write("<u>Wall section input</u>",unsafe_allow_html=True)
                    tw = (Pier_forces['b'])#.prefix('unity')
                    st.write("Width (mm):", tw)
                    Hwe = Pier_forces['H']
                    st.write("Effective height (mm):", Hwe)
                    Lw = (Pier_forces['d'])#.prefix('unity')
                    st.write("Length (mm):", Lw)

                    pw = 0.0025
                    st.write("Minimum reo ratio in horizontal & vertical direction(cl11.7.1):", pw)
                    fsy = 500
                    st.write("Assumed steel yield strength (MPa):", fsy)
                    Horz_bar_dia = st.selectbox("Horizontal bar diameter (mm)",options=('10','12','16','20','24','28','32'))
                    Horz_bar_spc = st.selectbox("Horizontal bar spcaing (mm)",options=('100','150','200','250','300','350','400'))
                    Vert_bar_dia = st.selectbox("Vertical bar diameter (mm)",options=('10','12','16','20','24','28','32'))
                    Vert_bar_spc = st.selectbox("Vertical bar spcaing (mm)",options=('100','150','200','250','300','350','400'))
                    
                    

                
                
                #COMPRESSION CAPACITY CHECK
                with col1:
                    st.write('<p style="color: green;"><b>1. Design axial capacity check (φNu)</b></p>',unsafe_allow_html=True)
                    #st.caption(""" ##### Design Assumptions: 

                #(a): Vertical and horizontal reinforcement is provided on both wall faces and divided equally between the two wall faces.

                #(b): Have a ratio of effective height to thickness that does not exceed 30 for doubly reinforced walls.""")

                    #if Soil_classification == "De - Deep or soft soil":
                        #st.markdown("Simplified design method for compression forces does not apply (cl.11.5.2(c)), design wall as column as per AS3600:2018 Section 10")
                    #elif Soil_classification == "Ee - Very soft soil":
                        #st.markdown("Simplified design method for compression forces does not apply (cl.11.5.2(c)), design wall as column as per AS3600:2018 Section 10")
                    #else:
                        #st.markdown("Simplified design method for compression forces applies (cl.11.5)")
                    concrete_strength = st.selectbox("Concrete strength f'c (MPa)",options=('20','25','32','40','50','65','80','100'))
                    try:
                        with col1:
                            @handcalc()
                            def wall_segment(tw: float) -> float:
                                """ 
                                Calculates division of wall into segements for compression check, (uses tw:Lw ratio of 1:4)
                                """
                                Sg = (4*tw)
                                return Sg
                        with col2:
                            Sg_latex, Sg_value = wall_segment(tw)
                            st.markdown("Length of wall segment:")
                            st.latex(Sg_latex)

                            @handcalc()
                            def eccentricity(tw: float) -> float:
                                """ 
                                Calculates the eccentricity of the vertical load in mm
                                """
                                e = 0.05*tw
                                return e
                        with col2:
                            e_latex, e_value = eccentricity(tw)
                            st.markdown("Eccentricity of vertical load(cl11.5.4):")
                            st.latex(e_latex)

                            @handcalc()
                            def additional_eccentricity(tw: float, Hwe: float) -> float:
                                """ 
                                Calculates the additional eccentricity of the vertical load in mm
                                """
                                ea = ((Hwe)**2)/(2500*tw)
                                return ea
                        with col2:
                            ea_latex, ea_value = additional_eccentricity(tw,Hwe)
                            st.markdown("Additonal eccentricity of vertical load(cl11.5.3):")
                            st.latex(ea_latex)

                            fc = float(concrete_strength) * si.MPa
                            e_latex, e_value = eccentricity(tw)
                            e = float(e_value) * si.mm
                            ea_latex, ea_value = additional_eccentricity(tw,Hwe)
                            ea = float(ea_value) * si.mm
                            tw = Pier_forces['b'] * si.mm
                            Sg_latex, Sg_value = wall_segment(tw)
                            Sg = Sg_value
                            @handcalc()
                            def ultimate_strength(tw: float, ea: float, e: float, fc: float) -> float:
                                """ 
                                Calculates the ultimate compression strength of wall segment
                                """
                                Nu = ((0.65*((tw-1.2*e-2*ea)*0.6*fc))*Sg).prefix('k')
                                return Nu
                        with col2:
                            Nu_latex, Nu_value = ultimate_strength(tw,ea,e,fc)
                            st.markdown("Compression capacity of wall segment (cl.11.5.3):")
                            st.latex(Nu_latex)

                            s = Pier_forces['Net compression stress'] * si.MPa
                            Sg_latex, Sg_value = wall_segment(tw)
                            Sg = Sg_value
                            @handcalc()
                            def axial_load(tw: float, s: float) -> float:
                                """ 
                                Calculates the compression force on the wall from net compression stress on wall segment
                                """
                                P = (tw*s*Sg).prefix('k')
                                return P
                        with col2:
                            P_latex, P_value = axial_load(tw,s)
                            st.markdown("Compression force on wall segment:")
                            st.latex(P_latex)
                        with col1:
                            P_latex, P_value = axial_load(tw,s)
                            P = round(float(P_value),1)
                            st.write("Compression force on wall segment, P (kN):", P)
                            Nu_latex, Nu_value = ultimate_strength(tw,ea,e,fc)
                            Nu = round(float(Nu_value),1)
                            st.write("Compression capacity of wall segment, Nu (kN)):", Nu)
                            if P > Nu:
                                st.write('<p style="color: red;">Compression capacity of wall exceeded, NG!!</p>', unsafe_allow_html=True)
                            else:
                                st.write('<p style="color: green;">Wall segment compression capacity, OKAY!!</p>', unsafe_allow_html=True)
                        
                        #INPLANE SHEAR CHECK
                        #1. Shear strength excluding wall reinforcement

                        with col1:
                            st.write('<p style="color: green;"><b>2. In-plane shear capacity check (φVu)</b></p>',unsafe_allow_html=True)
                            V = abs(Pier_forces['V2(Max V2)'])
                            st.write("Shear force in wall (kN):", V)
                            st.markdown("(a)Shear strength excluding wall reinforcement(cl11.6.3)")

                            Lw = Pier_forces['d'] * si.mm
                            Hw = Pier_forces['H'] * si.mm
                            tw = Pier_forces['b'] * si.mm
                            fc = float(concrete_strength) * si.MPa
                            @handcalc()
                            def Shear_strength_ex_reo1(tw: float, Lw: float, Hw: float, fc: float) -> float:
                                """
                                Returns the shear strength of the wall excluding wall reinforcement where Hw/Lw <= 1
                                """
                                Vuc = (((0.66*math.sqrt(fc)*si.MPa)-0.21*(Hw/Lw)*(math.sqrt(fc)*si.MPa))*0.8*Lw*tw).prefix('k')
                                return Vuc
                        with col1:
                            if Hw/Lw < 1 or Hw/Lw == 1:
                                Vuc_latex, Vuc_value = Shear_strength_ex_reo1(tw,Lw,Hw,fc)
                                Vuc = round(float(Vuc_value),2)
                                st.write("In-plane capacity excluding wall reinforcement, Vuc (kN)):", Vuc)
                        with col2:
                            if Hw/Lw < 1 or Hw/Lw == 1:
                                Vuc_latex, Vuc_value = Shear_strength_ex_reo1(tw,Lw,Hw,fc)
                                st.markdown("In-plane capacity excluding wall reinforcement:")
                                st.latex(Vuc_latex)

                            @handcalc()
                            def Shear_strength_ex_reo2(tw: float, Lw: float, Hw: float, fc: float) -> float:
                                """
                                Returns the shear strength of the wall excluding wall reinforcement where Hw/Lw > 1
                                """
                                Vuc = (((0.05*(math.sqrt(fc))*si.MPa)+((0.1*(math.sqrt(fc))*si.MPa)/((Hw/Lw)-1)))*0.8*Lw*tw).prefix('k')
                                return Vuc
                        with col1:
                            if Hw/Lw > 1:
                                Vuc_latex, Vuc_value = Shear_strength_ex_reo2(tw,Lw,Hw,fc)
                                Vuc = round(float(Vuc_value),2)
                                st.write("In-plane capacity excluding wall reinforcement, Vuc (kN)):", Vuc)
                        with col2:
                            if Hw/Lw > 1:
                                Vuc_latex, Vuc_value = Shear_strength_ex_reo2(tw,Lw,Hw,fc)
                                st.markdown("In-plane capacity excluding wall reinforcement:")
                                st.latex(Vuc_latex)

                        #2. Contribution to shear strength by wall reinforcement
                        with col1:
                            st.markdown("(b) Contribution to shear strength by wall reinforcement(cl11.6.4)")
                            
                        @handcalc()
                        def hor_reo_ratio(Horz_bar_dia: float, Horz_bar_spc: float,tw: float):
                            """
                            Returns the reo ratio in the horizontal direction
                            """
                            pw2 = ((math.pi*float(Horz_bar_dia)**2/4)*(1000/float(Horz_bar_spc))*2)/(1000*float(tw))
                            return pw2
                        with col1:
                            pw2_latex, pw2_value = hor_reo_ratio(Horz_bar_dia,Horz_bar_spc,tw)
                            pw2 = round(float(pw2_value),5)
                            st.write("Horizontal reo ratio(pw)", pw2)
                            if pw2 < 0.0025:
                                st.write('<p style="color: red;">Horizontal reo ratio is less than 0.0025, NG!!</p>', unsafe_allow_html=True)
                            #else:
                                #st.write('<p style="color: green;">Wall segment compression capacity, OKAY!!</p>', unsafe_allow_html=True)

                            @handcalc()
                            def Shear_strength_with_reo(pw: float, Lw: float, fsy: float) -> float:
                                """
                                Returns the contribution to shear strength by wall reinforcement
                                """
                                Vus = (max(0.0025,((pw2 * fsy*si.MPa)*0.8*Lw*tw))).prefix('k')
                                return Vus
                        with col1:
                            Vus_latex, Vus_value = Shear_strength_with_reo(pw,Lw,fsy)
                            Vus = round(float(Vus_value),2)
                            st.write("In-plane capacity contribution from wall reinforcement, Vus (kN)):", Vus)
                        with col2:
                            Vus_latex, Vus_value = Shear_strength_with_reo(pw,Lw,fsy)
                            st.markdown("In-plane capacity contribution from wall reinforcement:")
                            st.latex(Vus_latex)

                            phi = 0.65
                            @handcalc()
                            def strength_in_shear(Vuc: float, Vus: float) -> float:
                                """
                                Returns the design strength of the wall subjected to in-plane shear forces
                                """
                                Vu = (phi*(Vuc*si.kN + Vus*si.kN)).prefix('k')
                                return Vu
                        with col1:
                            Vu_latex, Vu_value = strength_in_shear(Vuc,Vus)
                            Vu = round(float(Vu_value),2)
                            st.write("Wall strength in shear, Vu (kN):", Vu)
                            if Vu < V:
                                st.write('<p style="color: red;">Shear capacity exceeded, NG!!</p>', unsafe_allow_html=True)
                            else:
                                st.write('<p style="color: green;">Shear demand, OKAY!!</p>', unsafe_allow_html=True)
                        with col2:
                            Vu_latex, Vu_value = strength_in_shear(Vuc,Vus)
                            st.markdown("Wall strength in shear:")
                            st.latex(Vu_latex)

                        #3. Detailing
                        with col1:
                            st.write('<p style="color: green;"><b>3. Reinforcement Detailing</b></p>',unsafe_allow_html=True)
                            st.markdown("Vertical Reinforcement: Minimum vertical reinforcement is required.")
                        with col1:
                            st.write("Minimum reo ratio in vertical direction(Cl11.7.1):", pw)
                            fsy = 500

                        @handcalc()
                        def vert_reo_ratio(Vert_bar_dia: float, Vert_bar_spc: float,tw: float) -> float:
                            """
                            Returns the reo ratio in the horizontal direction
                            """
                            pw3 = ((math.pi*float(Vert_bar_dia)**2/4)*((1000/float(Vert_bar_spc))*2)/(1000*float(tw)))
                            return pw3
                        with col1:
                            pw3_latex, pw3_value = vert_reo_ratio(Vert_bar_dia,Vert_bar_spc,tw)
                            pw3 = round(float(pw3_value),5)
                            st.write("Vertical bars reo ratio(pw)", pw3)
                            if pw3 < 0.0025:
                                st.write('<p style="color: red;">Vertical reo ratio is less than 0.0025, NG!!</p>', unsafe_allow_html=True)
                        with col1:
                            st.markdown("- Restraint of Vertical Reinforcement (CL11.7.4):")
                        fc = float(concrete_strength)
                        with col1:
                            if fc<51:
                                st.write('<p style="color: green;">Restraint not required for vertical bars (CL11.7.4(c))</p>', unsafe_allow_html=True)
                        #with col1:
                            elif fc>51 and P > 0.5 * Nu:
                                st.markdown('<p style="color: red;">Restraint required for vertical bars, detail in accordance with CL14.5.4 (CL11.7.4(d)(ii))</p>', unsafe_allow_html=True)
                                restrained_distance = max(Sg,(Pier_forces['H']/6))
                                st.markdown('<p style="color: red;">Provide restraint at each end of the clear height of the wall segment within the storey, refer to CL14.5.4 for fitment size and spacing.</p>', unsafe_allow_html=True)
                                st.markdown('<p style="color: red;">Distance from each end of the clear height of segment to be restrained:</p>', unsafe_allow_html=True)
                                st.write(restrained_distance)
                            else:
                                st.write('<p style="color: green;">Restraint not required for vertical bars (CL11.7.4(c))</p>', unsafe_allow_html=True)

                    except NameError:
                        st.markdown("No wall is subject to compression over its entire section, design all walls as a column(CL11.2.1).")
            
        with tab5:
            #Soil_classification = st.selectbox("Site soil classification:", options=('Ae - Strong rock','Be - Rock','Ce - Shallow soil', 'De - Deep or soft soil', 'Ee - Very soft soil'))
            if Soil_classification == "De - Deep or soft soil" or Soil_classification == "Ee - Very soft soil":
                st.markdown("Simplified design method for compression forces does not apply (CL11.5.2(c)), all walls to be design as columns as per Section 10.")
                df3 = df2
            else:
                df3=design_col
            df3.set_index(['Pier',df3.index], inplace=True)
            st.markdown("**Walls with tensile stresses in part of its section**")
            st.dataframe(df3)
            unique_stories = df3.index.get_level_values('Pier').unique()
            selected_pier = st.selectbox("Select a Pier:", unique_stories)
            unique_piers = df3.index.get_level_values('Story').unique()
            selected_story = st.selectbox("Select Story:", unique_piers)
            
            col1, col2 = st.columns([1,2])
            with col2:
                #Pier_forces2 = df.loc[(selected_pier, selected_story)]
                try:
                    Pier_forces_col = df3.loc[(selected_pier, selected_story)]
                    st.write("Selected Pier forces:")
                    st.write(Pier_forces_col)
                except KeyError:
                    st.write("Selected story and pier combination is not available.")

            with col1:
                st.write("<u>Wall section input</u>",unsafe_allow_html=True)
                tw = Pier_forces_col['b']
                st.write("Width (mm):", tw)
                b = Pier_forces_col['d']
                st.write("Length (mm):", b)
                reo_bar_size = st.selectbox("Reinforcement Bar Size (mm):",options=('10','12','16','20','24','28','32','36','40'))
                bar_area = (3.14*(float(reo_bar_size))**2)/4
                st.write("Bar area (mm2):", bar_area)
                right_bars = st.number_input (label="Number of bars on the right:",min_value=2,max_value=100,step=1)
                left_bars = st.number_input (label="Number of bars on the left:",min_value=2,max_value=100,step=1)
                if right_bars != left_bars:
                    st.write('<p style="color: red;">Number of bars on the right of the wall MUST equal number of bars on the left of the wall.</p>', unsafe_allow_html=True)
                #st.number_input (label="Right cover(mm):",min_value=5,max_value=100,step=5)
                #st.number_input (label="Left cover(mm):",min_value=5,max_value=100,step=5)
                cover_1 = st.number_input (label="Cover to reinforcement(mm):",min_value=5,max_value=100,step=5)
                #cover_2 = st.number_input (label="Bottom cover(mm):",min_value=5,max_value=100,step=5)
                concrete_fc = st.selectbox("Concrete strength, f'c (MPa)",options=('25','32','40','50','65','80','100'))
                fsy = 500
                st.write("Yield strength of reinforcing steel (MPa):", fsy)
            
            @handcalc()
            def alpha1(concrete_fc: float) -> float:
                """
                Returns the alpha1 value of the concrete compression block.
                """
                alpha = 1.0-0.003*float(concrete_fc)
                alpha1 = max(0.72, min(alpha, 0.85))
                return alpha1
            with col1:
                alpha1_latex, alpha1_value = alpha1(concrete_fc)
                alpha1 = round(float(alpha1_value),2)
                st.write("𝛼1:", alpha1)
            
            @handcalc()
            def alpha2(concrete_fc: float) -> float:
                """
                Returns the alpha2 value of the concrete compression block.
                """
                alpha = 1.0-0.003*float(concrete_fc)
                alpha2 = max(0.67, min(alpha, 0.85))
                return alpha2
            with col1:
                alpha2_latex, alpha2_value = alpha2(concrete_fc)
                alpha2 = round(float(alpha2_value),2)
                st.write("𝛼2:", alpha2)
            
            @handcalc()
            def gamma(concrete_fc: float) -> float:
                """
                Returns the gamma value of the concrete compression block.
                """
                gamma = 1.05-0.007*float(concrete_fc)
                gamma = max(0.67, min(gamma, 0.85))
                return gamma
            with col1:
                gamma_latex, gamma_value = gamma(concrete_fc)
                gamma = round(float(gamma_value),2)
                st.write("γ:", gamma)
            
            #SQUASH LOAD
        
            #1. At squash load point all steel are yeilded.
            #2. Concrete have reached the ultimate compressive stress (𝛼1f'c)
            with col2:
                st.write('<p style="color: green;"><b>1. Four points to determine the M-N interaction diagram</b></p>',unsafe_allow_html=True)
                st.write('<p style="color: green;"><b>A. Squash load</b></p>',unsafe_allow_html=True)
            tw = Pier_forces_col['b']*si.mm
            Lw = (Pier_forces_col['d']*si.mm).prefix('unity')
            fc = float(concrete_fc)*si.MPa
            @handcalc()
            def squash_load(fc: float,Lw: float, tw: float) -> float:
                """
                Returns the squash load of the wall in kN
                """
                Asc = bar_area*(left_bars+right_bars)*si.mm**2
                Nuo = 0.65*((alpha1 * fc * tw * Lw) + (Asc * fsy *si.MPa)).prefix('k')
                return Nuo
            with col2:
                Nuo_latex, Nuo_value = squash_load(fc,Lw,tw)
                Nuo = round(float(Nuo_value),2)
                st.write("Squash Load, Nuo (kN):", Nuo)
                st.write("Bending Moment, M* (kNm):", 0)
            # with col2:
            #     Nuo_latex, Nuo_value = squash_load(fc,Lw,tw)
            #     st.markdown("Squash Load, Nuo:")
            #     st.latex(Nuo_latex)
            
            

            #Decompression point
            
            #1. At decompression point extreme tensile steel has no strain
            #2. Concrete compressive fibre have reached ultimate striain at 0.003
            #The stress in concrete can be reqpresented using a rectangular stress block

            #Determine compression force in each layer of steel.
            with col2:
                st.write('<p style="color: green;"><b>B. Decompression point</b></p>',unsafe_allow_html=True)
            column_bars = int(right_bars)
            bar_layers = [f'layer {i}' for i in range(1, column_bars + 1 )]
            #st.write(bar_layers)

            Asc_per_layer = bar_area*2*si.mm**2
            reo_dia = float(reo_bar_size) * si.mm
            conc_cover = cover_1 *si.mm

            #@handcalc()
            def effective_depth(Lw: float, conc_cover: float, reo_dia: float) -> float:
                """
                Returns the effective depth of the section in mm
                """
                deff = (Lw - conc_cover - (10*si.mm) - reo_dia/2).prefix('unity')
                return deff
            deff = effective_depth(Lw, conc_cover, reo_dia)
            #st.write(deff)
            # with col1:
            #     deff_latex, deff_value = effective_depth(Lw,conc_cover,reo_dia)
            #     deff = round(float(deff_value),2)
            #     st.write("Effective depth, d:", deff)
            #with col2:
                #deff_latex, deff_value = effective_depth(Lw,conc_cover,reo_dia)
                #st.markdown("Effective depth, d:")
                #st.latex(deff_latex)

            #Determine the strain each layer of steel.
            spacing_bars = (Lw - (conc_cover * 2))/(right_bars - 1)
            #st.write(spacing_bars)
            
            def strain_per_layer(deff: float, conc_cover: float, bar_layers: list, spacing_bars: float) -> list:
                """
                Returns the strain in each layer of reinforcement
                """
                strains = []
                for i in range(len(bar_layers)):
                    deff_layer = deff - conc_cover - (i * spacing_bars)
                    es = (float(deff_layer  / deff) * 0.003)#/1000
                    if es < 0:
                        es = 0
                    else:
                        es = es
                    strains.append(es)
                return strains

            # strain_result = strain_per_layer(deff, conc_cover, bar_layers, spacing_bars)
            # st.write(strain_result)

            Es = 200000 * si.MPa
            def steel_compr_force(bar_area: float, strains: list) -> list:
                """
                Returns the compression force in each layer of reinforcement in kN
                """
                force_layer = []
                for es in strains:
                    force = (bar_area*si.mm**2)*2 * es * Es
                    force_layer.append(force)
                return force_layer
            #force_layer = steel_compr_force(bar_area,strains=strain_per_layer(deff, conc_cover, bar_layers, spacing_bars))
            #st.write(force_layer)

            @handcalc()
            def Concrete_Compr_force_resultant(gamma: float, deff: float, alpha2: float, fc: float, tw: float) -> float:
                """
                Returns compression force resultant in the concrete in kN
                """
                ku = 1
                Cc =  (gamma * ku * deff * alpha2 * fc * tw).prefix('k')
                return Cc
            with col2:
                Cc_latex, Cc_value = Concrete_Compr_force_resultant(gamma,deff,alpha2,fc,tw)
                Cc = round(float(Cc_value),2)
                #st.write("Concrete resultant compression force, Cc (kN):", Cc)
            #with col2:
                #Cc_latex, Cc_value = Concrete_Compr_force_resultant(gamma,deff,alpha2,fc,tw)
                #st.markdown("Concrete resultant compression force, Cc:")
                #st.latex(Cc_latex)

            @handcalc()
            def steel_Compr_force_resultant(force_layer: list) -> float:
                """
                Returns compression force resultant in the steel layers in kN
                """
                Ns = (sum(force_layer)).prefix('k')
                return Ns
            with col2:
                force_layer = steel_compr_force(bar_area,strains=strain_per_layer(deff, conc_cover, bar_layers, spacing_bars))
                Ns_latex, Ns_value = steel_Compr_force_resultant(force_layer)
                Ns = round(float(Ns_value),2)
                #st.write("Steel resultant compression force, Ns (kN):", Ns)

            @handcalc()
            def total_compr_force(force_layer: list, Cc: float) -> float:
                """
                Returns the total compression force in the section in kN
                """
                N = 0.65*(sum(force_layer) + Cc*si.kN).prefix('k')
                return N
            with col2:
                force_layer = steel_compr_force(bar_area,strains=strain_per_layer(deff, conc_cover, bar_layers, spacing_bars))
                N_latex, N_value = total_compr_force(force_layer ,Cc)
                N = round(float(N_value),2)
                st.write("Net Axial force,N* (kN):", N)

            #Determine lever arm of each bar to the plastic centrioid
                
            def pc(Lw: float, conc_cover: float) -> float:
                """
                Returns the plastic centroid of the concrete section in mm
                """
                pc = (Lw-(2*conc_cover))/2
                return pc
            pc = pc(Lw, conc_cover)
            #st.write(pc)

            def LeverArm(pc: float, spacing_bars: float, bar_layers: list) -> float:
                """
                Returns the distance of the bar layer to the plastic centroid of the section in mm
                """
                leverarm = []
                for i in range(len(bar_layers)):
                    LA = abs(pc - (i * spacing_bars))
                    leverarm.append(LA)
                return leverarm
            
            leverarm = LeverArm(pc, spacing_bars, bar_layers)
            # st.write(leverarm)

            def cal_moment(force_layer: list, leverarm: list) -> list:
                moment = []
                for i in range(len(force_layer)):
                    moment.append(force_layer[i]*leverarm[i])
                return moment
            #moment = cal_moment(force_layer, leverarm)
            #st.write(moment)

            @handcalc()
            def sum_moment(moment: list, pc: float, Cc: float, deff: float) -> float:
                """
                Returns the total bending moment due to all the forces about the plastic centroid in the section in kNm
                """
                M = ((sum(moment) + ((pc-(deff/3))*Cc*si.kN))*0.65).prefix('k')
                return M
            with col2:
                moment = cal_moment(force_layer, leverarm)
                M_latex, M_value = sum_moment(moment, pc, Cc, deff)
                M = round(float(M_value),2)
                st.write("Bending Moment, M* (kNm):", M)


            #Balanced point
            
            #1. At balanced point, extreme tensile steel just yielded (strain = 0.0025)
            #2. Concrete compressive fibre have reached ultimate striain at 0.003, ku = 0.545, kud = 0.545d
            #The stress in concrete cab be reqpresented using a rectangular stress block

            with col2:
                st.write('<p style="color: green;"><b>C. Balanced point</b></p>',unsafe_allow_html=True)
            @handcalc()
            def Concrete_Compr_force_resultant2(gamma: float, deff: float, alpha2: float, fc: float, tw: float) -> float:
                """
                Returns compression force resultant in the concrete at balanced point in kN
                """
                ku = 0.545
                Cc2 =  (gamma * ku * deff * alpha2 * fc * tw).prefix('k')
                return Cc2
            with col2:
                Cc2_latex, Cc2_value = Concrete_Compr_force_resultant2(gamma,deff,alpha2,fc,tw)
                Cc2 = round(float(Cc2_value),2)
                #st.write("Concrete resultant compression force, Cc (kN):", Cc2)


            def strain_per_layer2(deff: float, conc_cover: float, bar_layers: list, spacing_bars: float) -> list:
                """
                Returns the strain in each layer of reinforcement
                """
                strains2 = []
                for i in range(len(bar_layers)):
                    deff_layer = deff*0.545 - conc_cover - (i * spacing_bars)
                    es = (float(deff_layer  / (deff*0.545)) * 0.003)#/1000
                    #if es < 0:
                        #es = 0
                    #else:
                        #es = es
                    strains2.append(es)
                return strains2
            # strain_result = strain_per_layer2(deff, conc_cover, bar_layers, spacing_bars)
            # st.write(strain_result)

            def steel_force(bar_area: float, strains2: list) -> list:
                """
                Returns the force in each layer of reinforcement in kN
                """
                strains2 = strain_per_layer2(deff, conc_cover, bar_layers, spacing_bars)
                force_layer2 = []
                for es in strains2:
                    force2 = (bar_area*si.mm**2)*2 * es * Es
                    force_layer2.append(force2)
                return force_layer2
            force_layer2 = steel_force(bar_area,strains2=strain_per_layer2(deff, conc_cover, bar_layers, spacing_bars))
            #st.write(force_layer2)

            @handcalc()
            def total_force(force_layer2: list, Cc2: float) -> float:
                """
                Returns the total compression force in the section in kN
                """
                force_layer2 = steel_force(bar_area,strains2=strain_per_layer2(deff, conc_cover, bar_layers, spacing_bars))
                tensile_forces = sum([x for x in force_layer2 if x < 0])
                compr_forces = sum([x for x in force_layer2 if x > 0])
                if tensile_forces > compr_forces:
                    net_axial = abs(tensile_forces) - compr_forces
                if tensile_forces < compr_forces:
                    net_axial = compr_forces - abs(tensile_forces)
                N2 = 0.65*(net_axial + Cc2*si.kN).prefix('k')
                return N2
            with col2:
                force_layer2 = steel_force(bar_area,strains2=strain_per_layer2(deff, conc_cover, bar_layers, spacing_bars))
                N2_latex, N2_value = total_force(force_layer ,Cc2)
                N2 = round(float(N2_value),2)
                st.write("Net Axial force,N* (kN):", N2)


            def cal_moment2(force_layer2: list, leverarm: list) -> list:
                moment2 = []
                for i in range(len(force_layer2)):
                    moment2.append(force_layer2[i]*leverarm[i]*0.65)
                return moment2
            #moment2 = cal_moment2(force_layer2, leverarm)
            #st.write(moment2)

            @handcalc()
            def sum_moment2(moment2: list, pc: float, Cc2: float, deff: float) -> float:
                """
                Returns the total bending moment due to all the forces about the plastic centroid in the section in kNm
                """
                abs_values = [abs(x) for x in moment2]
                M2 = (((sum(abs_values))*0.65) + (((pc-((deff*0.545)/3))*(Cc2*si.kN))*0.65)).prefix('k')
                return M2
            with col2:
                moment2 = cal_moment2(force_layer2, leverarm)
                M2_latex, M2_value = sum_moment2(moment2, pc, Cc2, deff)
                M2 = round(float(M2_value),2)
                st.write("Bending Moment,M* (kNm):", M2)


            #Pure bending
            #1. At pure bending point, extreme tensile steel has already yielded (strain > 0.0025).
            #2. Concrete compressive fibre have reached ultimate striain at 0.003 and ku is unknown.
            #3. The stress in concrete can be represented using a rectangular stress block.
                
            with col2:
                st.write('<p style="color: green;"><b>D. Pure bending</b></p>',unsafe_allow_html=True)

            def det_ku3(deff: float, conc_cover: float, bar_layers: list, spacing_bars: float) ->float:
                """
                Returns the value of ku3 where the sum of forces in the concrete section equals 0
                """
                ku3_values = np.round(np.linspace(0.001, 0.5, num=1000),4)
                index = 0
                strains3 = []

                while index < len(ku3_values):
                    ku3 = ku3_values[index]
                    force_layer3 = []
                    condition_met = False
                    strains3 = []

                    for i in range(len(bar_layers)):
                        deff_layer = deff * ku3 - conc_cover - (i * spacing_bars)
                        es = (float(deff_layer  / (deff*ku3)) * 0.003)
                        strains3.append(es)
                        for es in strains3:
                            force = (((bar_area * si.mm**2)) * 2 *es *Es).prefix('k')
                            force_layer3.append(force)
                    Cc3 = (gamma * ku3 * deff * alpha2 * fc *tw).prefix('k')
                    if -50 <= float(sum(force_layer3) + Cc3) <=50:
                        condition_met = True
                        break
                        st.write(f'ku: {ku3}, condition_met: {condition_met}')
                    if condition_met:
                        break
                    index += 1
                return ku3
            
            ku3 = det_ku3(deff, conc_cover, bar_layers, spacing_bars)
            #st.write(ku3)


            
            def strain_per_layer3(deff: float, conc_cover: float, bar_layers: list, spacing_bars: float, ku3: float) -> list:
                """
                Returns the strain in each layer of reinforcement
                """
                strains4 = []
                for i in range(len(bar_layers)):
                    deff_layer = deff * ku3 - conc_cover - (i * spacing_bars)
                    es = (float(deff_layer  / (deff*ku3)) * 0.003)#/1000
                    #if es < 0:
                        #es = 0
                    #else:
                        #es = es
                    strains4.append(es)
                return strains4
            # strain_result = strain_per_layer3(deff, conc_cover, bar_layers, spacing_bars, ku3)
            # st.write(strain_result)


            @handcalc()
            def Concrete_Compr_force_resultant3(gamma: float, deff: float, alpha2: float, fc: float, tw: float) -> float:
                """
                Returns compression force resultant in the concrete at pure bending point in kN
                """
                Cc3 =  (gamma * ku3 * deff * alpha2 * fc * tw).prefix('k')
                return Cc3
            with col2:
                Cc3_latex, Cc3_value = Concrete_Compr_force_resultant3(gamma,deff,alpha2,fc,tw)
                Cc3 = round(float(Cc3_value),2)
                #st.write("Concrete resultant compression force, Cc (kN):", Cc3)

            def steel_force3(bar_area: float, strains3: list) -> list:
                """
                Returns the force in each layer of reinforcement in kN
                """
                force_layer3 = []
                for es in strains3:
                    force3 = ((bar_area*si.mm**2)*2*es*Es).prefix('k')
                    force_layer3.append(force3)
                return force_layer3
            force_layer3 = steel_force3(bar_area,strains3=strain_per_layer3(deff, conc_cover, bar_layers, spacing_bars, ku3))
            # st.write(force_layer3)

            def cal_moment3(force_layer3: list, leverarm: list) -> list:
                moment3 = []
                for i in range(len(force_layer3)):
                    moment3.append(force_layer3[i]*leverarm[i])
                return moment3
            moment3 = cal_moment3(force_layer3, leverarm)
            # st.write(moment3)

            @handcalc()
            def sum_moment3(moment3: list, pc: float, Cc3: float, deff: float) -> float:
                """
                Returns the total bending moment due to all the forces about the plastic centroid in the section in kNm
                """
                abs_values = [abs(x) for x in moment3]
                M3 = (((sum(abs_values))*0.6) + (((pc-((deff*ku3)/3))*(Cc3*si.kN))*0.6)).prefix('k')
                return M3
            with col2:
                force_layer3 = steel_force3(bar_area,strains3=strain_per_layer3(deff, conc_cover, bar_layers, spacing_bars, ku3))
                moment3 = cal_moment3(force_layer3, leverarm)
                M3_latex, M3_value = sum_moment3(moment3, pc, Cc3, deff)
                M3 = round(float(M3_value),2)
                st.write("Net Axial force,N* (kN):", 0)
                st.write("Bending Moment,M* (kNm):", M3)
                

            

            #M-N interaction graph plot
            with col2:
                #st.write('<p style="color: green;"><b>M-N Interaction diagram</b></p>',unsafe_allow_html=True)
            #Squash_load,
                #N_s = squash_load(fc,Lw,tw)
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=[0, float(M),float(M2),float(M3)],
                        y=[float(Nuo),float(N),float(N2), 0],
                        name = 'M-N Curve',
                        line_shape = 'spline'
                        )
                        
                        )
                fig.add_trace(
                    go.Line(
                        x=[0,abs(Pier_forces_col['M3(Compr)'])],
                        y=[0,abs(Pier_forces_col['P(Compr)'])],
                        name = 'Max Compression Case'
                        )
                        )
                fig.add_trace(
                    go.Line(
                        x=[0,abs(Pier_forces_col['M3(Max M3)'])],
                        y=[0,abs(Pier_forces_col['P(Max M3)'])],
                        name = 'Max M3 Case'
                        )
                        )
                fig.update_layout(
                    title = 'Wall M-N interaction diagram',
                    xaxis_title='Bending Moment (kNm)', 
                    yaxis_title='Axial Force (kN)',
                    xaxis=dict(tickformat=',.0f'),
                    yaxis=dict(tickformat=',.0f'),
                    #height = 800
                    )
            
                st.plotly_chart(fig)

            #Column slenderness check
            N = abs(Pier_forces_col['P(Compr)'])
            Hw2 = (Pier_forces_col['H']*si.mm).prefix('unity')
            Lw = (Pier_forces_col['d']*si.mm).prefix('unity')
            def alphac(N: float, Nuo: float, Hw: float) -> float:
                """
                Return the alphac value of the wall.
                """
                #alphac = N/(0.6*Nuo)
                if N/(0.6*Nuo) < 0.15:
                    alphac = math.sqrt(1/((3.5*Hw2)/(0.6*Nuo)))
                else:
                    alphac = math.sqrt(2.25-((2.5*N)/(0.6*Nuo)))
                return alphac
            alphac = alphac(N, Nuo, Hw)
            #st.write (alphac)

            M11 = 0.1*abs(Pier_forces_col['M3(Compr)'])
            M22 = abs(Pier_forces_col['M3(Compr)'])

            #@handcalc()
            def shortcolumn(Hw: float, alphac: float,fc: float, M11: float, M22: float) -> float:
                M11M22 = M11/M22
                req1 = Hw2/(Lw/3)
                req2 = alphac*(38-(fc/15))*(1+M11M22)
                if req1 <= max(25,req2):
                    st.write("Wall is STOCKY, no moment magnification required!")
                else:
                    st.write('Wall is SLENDER, moment magnification required!')
                return shortcolumn
            #slendercheck = shortcolumn(Hw, alphac,fc, M11, M22)
            #st.write(slendercheck)

            with col2:
                st.write('<p style="color: green;"><b>Slenderness check</b></p>',unsafe_allow_html=True)
                slendercheck = shortcolumn(Hw, alphac,fc, M11, M22)
                #st.write("Slenderness check:", slendercheck)
            

            #INPLANE SHEAR CHECK
                        #1. Shear strength excluding wall reinforcement

            with col1:
                st.write('<p style="color: green;"><b>2. In-plane shear capacity check (φVu)</b></p>',unsafe_allow_html=True)
                V = abs(Pier_forces_col['V2(Max V2)'])
                st.write("Shear force in wall (kN):", V)
                st.markdown("(a)Shear strength excluding wall reinforcement(cl11.6.3)")

                Lw = Pier_forces_col['d'] * si.mm
                Hw = Pier_forces_col['H'] * si.mm
                tw = Pier_forces_col['b'] * si.mm
                fc = float(concrete_fc)*si.MPa
                @handcalc()
                def Shear_strength_ex_reo2(tw: float, Lw: float, Hw: float, fc: float) -> float:
                    """
                    Returns the shear strength of the wall excluding wall reinforcement where Hw/Lw <= 1
                    """
                    Vuc = (((0.66*math.sqrt(fc)*si.MPa)-0.21*(Hw/Lw)*(math.sqrt(fc)*si.MPa))*0.8*Lw*tw).prefix('k')
                    return Vuc
            with col1:
                if Hw/Lw < 1 or Hw/Lw == 1:
                    Vuc_latex, Vuc_value = Shear_strength_ex_reo2(tw,Lw,Hw,fc)
                    Vuc = round(float(Vuc_value),2)
                    st.write("In-plane capacity excluding wall reinforcement, Vuc (kN)):", Vuc)
            with col2:
                if Hw/Lw < 1 or Hw/Lw == 1:
                    Vuc_latex, Vuc_value = Shear_strength_ex_reo2(tw,Lw,Hw,fc)
                    st.markdown("In-plane capacity excluding wall reinforcement:")
                    st.latex(Vuc_latex)

                @handcalc()
                def Shear_strength_ex_reo3(tw: float, Lw: float, Hw: float, fc: float) -> float:
                    """
                    Returns the shear strength of the wall excluding wall reinforcement where Hw/Lw > 1
                    """
                    Vuc = (((0.05*(math.sqrt(fc))*si.MPa)+((0.1*(math.sqrt(fc))*si.MPa)/((Hw/Lw)-1)))*0.8*Lw*tw).prefix('k')
                    return Vuc
            with col1:
                if Hw/Lw > 1:
                    Vuc_latex, Vuc_value = Shear_strength_ex_reo3(tw,Lw,Hw,fc)
                    Vuc = round(float(Vuc_value),2)
                    st.write("In-plane capacity excluding wall reinforcement, Vuc (kN)):", Vuc)
            with col2:
                if Hw/Lw > 1:
                    Vuc_latex, Vuc_value = Shear_strength_ex_reo3(tw,Lw,Hw,fc)
                    st.markdown("In-plane capacity excluding wall reinforcement:")
                    st.latex(Vuc_latex)

            #2. Contribution to shear strength by wall reinforcement
            with col1:
                st.markdown("(b) Contribution to shear strength by wall reinforcement(cl11.6.4)")
                pw = 0.0025
                st.write("Minimum reo ratio in horizontal direction(cl11.7.1):", pw)
                fsy = 500
                st.write("Assumed steel yield strength (MPa):", fsy)
                Horz_bar_dia2 = st.selectbox("Horz. bar diameter (mm)",options=('10','12','16','20','24','28','32'))
                Horz_bar_spc2 = st.selectbox("Horz. bar spacing (mm)",options=('100','150','200','250','300','350','400'))
            @handcalc()
            def hor_reo_ratio2(Horz_bar_dia2: float, Horz_bar_spc: float,tw: float):
                """
                Returns the reo ratio in the horizontal direction
                """
                pw3 = ((math.pi*float(Horz_bar_dia2)**2/4)*(1000/float(Horz_bar_spc2))*2)/(1000*float(tw))
                return pw3
            with col1:
                pw3_latex, pw3_value = hor_reo_ratio2(Horz_bar_dia2,Horz_bar_spc2,tw)
                pw3 = round(float(pw3_value),5)
                st.write("Horizontal reo ratio(pw)", pw3)
                if pw3 < 0.0025:
                    st.write('<p style="color: red;">Horizontal reo ratio is less than 0.0025 (cl11.7.1), NG!!</p>', unsafe_allow_html=True)
                #else:
                    #st.write('<p style="color: green;">Wall segment compression capacity, OKAY!!</p>', unsafe_allow_html=True)
            
            
            spacing_bars2 = ((Lw - (conc_cover * 2))/(right_bars - 1)).prefix('m')
            #st.write(spacing_bars2)
            @handcalc()
            def vert_reo_ratio(reo_bar_size: float, spacing_bars2: float,tw: float):
                """
                Returns the reo ratio in the vertical direction
                """
                pw4 = ((math.pi*float(reo_bar_size)**2/4)*(1000/float(spacing_bars2))*2)/(1000*float(tw))
                return pw4
            with col1:
                pw4_latex, pw4_value = vert_reo_ratio(reo_bar_size, spacing_bars2,tw)
                pw4 = round(float(pw4_value),5)
                st.write("Vertical reo ratio(pw)", pw4)
                if pw4 < 0.0025:
                    st.write('<p style="color: red;">Vertical reo ratio is less than 0.0025 (cl11.7.1), NG!!</p>', unsafe_allow_html=True)

            @handcalc()
            def reo_ratio_for_shear(pw3: float, pw4: float) -> float:
                """
                Returns the reo ratio to be used for contribution of steel to the ultimate shear strength of a wall by wall reinforcement(Vus)
                """
                if Hw/Lw < 1 or Hw/Lw == 1:
                    pw_vus = min(pw4,pw3)
                if Hw/Lw > 1:
                    pw_vus = pw3
                return pw_vus
            pw_vus = reo_ratio_for_shear(pw3,pw4)

            @handcalc()
            def Shear_strength_with_reo2(pw_vus: float, Lw: float, fsy: float, tw: float) -> float:
                """
                Returns the contribution to shear strength by wall reinforcement
                """
                Vus2 = (pw_vus * fsy*si.MPa)*0.8*Lw*tw.prefix('k')
                return Vus2
            with col1:
                Vus2_latex, Vus2_value = Shear_strength_with_reo2(pw3,Lw,fsy,tw)
                Vus2 = round(float(Vus2_value),2)
                st.write("In-plane capacity contribution from wall reinforcement, Vus (kN)):", Vus2)
            with col2:
                Vus2_latex, Vus2_value = Shear_strength_with_reo2(pw,Lw,fsy,tw)
                st.markdown("In-plane capacity contribution from wall reinforcement:")
                st.latex(Vus2_latex)

                phi = 0.65
            @handcalc()
            def strength_in_shear2(Vuc2: float, Vus2: float) -> float:
                """
                Returns the design strength of the wall subjected to in-plane shear forces
                """
                Vu2 = (phi*(Vuc*si.kN + Vus2*si.kN)).prefix('k')
                return Vu2
            with col1:
                Vu2_latex, Vu2_value = strength_in_shear2(Vuc,Vus2)
                Vu2 = round(float(Vu2_value),2)
                st.write("Wall strength in shear, Vu (kN):", Vu2)
                if Vu2 < V:
                    st.write('<p style="color: red;">Shear capacity exceeded, NG!!</p>', unsafe_allow_html=True)
                else:
                    st.write('<p style="color: green;">Shear demand, OKAY!!</p>', unsafe_allow_html=True)
            with col2:
                Vu2_latex, Vu2_value = strength_in_shear2(Vuc,Vus2)
                st.markdown("Wall strength in shear:")
                st.latex(Vu2_latex)

            with col1:
                st.write('<p style="color: green;"><b>3. Reinforcement detailing</b></p>',unsafe_allow_html=True)
                if float(fc)<51:
                    if pw4 < 0.01 and pw3 > 0.0025:
                        st.write('<p style="color: green;">Restraint to vertical reinforcement is not required</p>', unsafe_allow_html=True)
                    elif pw4 > 0.01 or pw3 < 0.0025:
                        st.write('<p style="color: red;">phi x Nuo check</p>', unsafe_allow_html=True)
                elif float(fc)>51:
                    st.write('<p style="color: red;">Provide restraint to vertical reinforcement in accordance with clause 14.5.4</p>', unsafe_allow_html=True)

                
                    
                


        


    with tab6:
        st.markdown("<p style='font-size:40px;'>Contact me</p>", unsafe_allow_html=True)

        st.markdown("**Name**: Emmanuel Eigbedion")

        st.markdown("**Email**: emmanuel.eigbedion@bgeeng.com")

        st.markdown("**Mobile**: 0406736008")
#except NameError:
            #st.markdown("Upload an Etabs File to continue")
except KeyError:
            st.markdown("Etabs files uploaded incorrectly")