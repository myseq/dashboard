import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

hdr1 = 'Baseline Compliance'
hdr1_desc = 'A Baseline Compliance Dashboard.'


def main():

    st.set_page_config(page_title='Dashboard', page_icon='📊')
    st.title(f':material/assured_workload: {hdr1} :material/assured_workload:')
    st.write(f'*{hdr1_desc}* :material/encrypted:')

    uploaded = st.file_uploader('Choosea a CSV file', type='csv')

    folder_path = "./"
    df = []

    # Load all CSV files
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):  # Check if the file is a CSV
            file_path = os.path.join(folder_path, file_name)
            df.append(pd.read_csv(file_path))

    if uploaded is None:
        st.write('Waiting on file upload... *(or loading CSV from local folder)*')
    else:
        df.append(pd.read_csv(uploaded))
        st.success(f'*Data loaded.*')

    if len(df) == 0:
        st.write("*No data available for the selected OS/status filters.*")
        return
    else:
        combined_df = pd.concat(df, ignore_index=True)
        combined_df.drop_duplicates(inplace=True)

    # Group by Hostname and OS
    groupby = (
        combined_df.groupby(["Hostname", "OS"])
        .apply(
            lambda x: {
                "pass_count": (x["Result"].str.lower() == "pass").sum(),
                "total_controls": len(x),
                "status": "comply" if (x["Result"].str.lower() == "pass").all() else "not_comply"
            },
            include_groups=False  
        )
        .apply(pd.Series)
    )

    groupby["compliance_ratio"] = groupby["pass_count"].astype(str) + "/" + groupby["total_controls"].astype(str)
    summary = groupby.reset_index()
    unique_os = summary["OS"].unique()
    unique_status = summary["status"].unique()

    st.sidebar.title('Filters')
    st.sidebar.subheader('*By OS :*')
    selected_os = [os for os in unique_os if st.sidebar.checkbox(os, value=True)]
    st.sidebar.subheader('*By Status :*')
    selected_status = [status for status in unique_status if st.sidebar.checkbox(status, value=True)]
    
    # Filter the DataFrame based on selected OS and status
    filtered_summary = summary[ summary["OS"].isin(selected_os) & summary["status"].isin(selected_status) ]

    if filtered_summary.empty:
        st.write("*No data available for the selected OS/status filters.*")
        return

    # Reset index and start from 1
    filtered_summary.reset_index(drop=True, inplace=True)
    filtered_summary.index += 1  # Start index from 1

    # Create a pie chart based on the filtered data
    compliance_counts = filtered_summary['status'].value_counts().reset_index()
    compliance_counts.columns = ['status', 'count']
    total_hosts = compliance_counts['count'].sum()

    # Donut chart on top
    st.subheader('Compliance Status')

    color_map = {'comply': 'green', 'not_comply': 'red'}
    compliance_counts['color'] = compliance_counts['status'].map(color_map)

    # Create the donut chart with forced colors
    fig = go.Figure(
        data=[
            go.Pie(
                labels=compliance_counts['status'],
                values=compliance_counts['count'],
                hole=0.4,
                marker=dict(colors=compliance_counts['color']),
                textinfo='label+percent',
            )
        ]
    )

    # Add the total count in the middle of the donut chart
    fig.update_layout(
        annotations=[
            dict(
                text=f"<b>{total_hosts}</b><br>Hosts",
                showarrow=False,
                font=dict(size=24)
            )
        ],
        title="Compliance Status Distribution",
    )

    # Display the donut chart
    st.plotly_chart(fig)

    selected_host = False
    # Interactive DataFrame with row selection via index
    st.subheader('Host Compliance Status')
    st.write('*Select host using the checkbox.*')

    st.session_state.df = filtered_summary
    selected_data = st.dataframe(st.session_state.df, width=680, key='data', on_select='rerun', selection_mode='single-row')

    if selected_data.selection:
        if selected_data.selection.get('rows'):
            selected_rows = selected_data.selection.get("rows")[0]
            selected_host = filtered_summary.iloc[selected_rows]['Hostname']
            selected_os = filtered_summary.iloc[selected_rows]['OS']
            selected_stat = filtered_summary.iloc[selected_rows]['status']
            st.write(f'Selection: *{selected_host}/{selected_os}/{selected_stat}*')
        else:
            st.write(f'Selection: *None*')
    else:
        st.write(f'*No data loaded.*')


    # Display the selected host's detailed controls
    if selected_host:
        host_summary = filtered_summary[filtered_summary['Hostname'] == selected_host]
        host_status = host_summary['status'].unique()[0]
        host_score = host_summary['compliance_ratio'].unique()[0]
        host_tctrls = host_summary['total_controls'].unique()[0]

        host_details = combined_df[combined_df['Hostname'] == selected_host]
        host_details.reset_index(drop=True, inplace=True)
        host_details.index += 1 # Start index from 1
        st.write(f'Hostname: ***{selected_host}***') 
        st.write(f'Status  : ***{host_status}*** *({host_score})*')
        st.dataframe(host_details)  # Show detailed controls for the selected host

        compliance_status_host = host_details['Result'].value_counts().reset_index()
        compliance_status_host.columns = ['status', 'count']

        color_map = {'pass': 'green', 'fail': 'red'}
        compliance_status_host['color'] = compliance_status_host['status'].map(color_map)

        # Create a pie chart for selected host
        fig_host = go.Figure(
            data=[
                go.Pie(
                    labels=compliance_status_host["status"],
                    values=compliance_status_host["count"],
                    hole=0.4,
                    marker=dict(colors=compliance_status_host["color"]),
                    textinfo="label+percent",
                )
            ]
        )

        # Add the total count in the middle of the donut chart
        fig_host.update_layout(
            annotations=[
                dict(
                    text=f"<b>{host_tctrls}</b><br>controls",
                    showarrow=False,
                    font=dict(size=18)
                )
            ],
            title=f'Status for {selected_host} : [ {host_status} ]',
        )

        st.plotly_chart(fig_host, use_container_width=True) # Display the pie chart

    else:
        st.write("*No host selected.*")

if __name__ == '__main__':

    main()

