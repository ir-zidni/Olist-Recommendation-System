import streamlit as st
import numpy as np
import pandas as pd

def load_data(data):

    df = pd.read_csv(data)
    return df

# Fungsi Untuk Sistem Rekomendasi
def rec_system(df, cluster_name = 'all', customer_state = 'all', n_rec = 10):

    ('''
    df              = dataset minimal harus memiliki kolom ['product_id', 'product_category', 'customer_state', 'cluster_name']
    cluster_name    = nama cluster dari customer segmentation
    customer_state  = nama state atau negara bagian, 'all' jika ingin melihat keseluruhan data
    n_rec = jumlah produk yang ingi direkomendsikan
    ''')

    if customer_state == 'all':

        if cluster_name == 'all':
            all_cluster = pd.DataFrame(df.groupby(['product_category'])['product_id'].value_counts()).rename({'product_id': 'purchase_count'}, axis = 1).reset_index().sort_values(by = 'purchase_count', ascending = False).reset_index(drop = True)

            return all_cluster[['product_category', 'product_id']].head(n_rec)

        elif cluster_name != 'all':
            
            df_cluster = df.loc[df['cluster_name'] == cluster_name]
            df_cluster = pd.DataFrame(df_cluster.groupby(['product_category'])['product_id'].value_counts()).rename({'product_id': 'purchase_count'}, axis = 1).reset_index().sort_values(by = 'purchase_count', ascending = False).reset_index(drop = True)
            
            return df_cluster[['product_category', 'product_id']].head(n_rec)

    elif customer_state != 'all':

        df = df.loc[df['customer_state'] == customer_state]

        if cluster_name == 'all':
            all_cluster = pd.DataFrame(df.groupby(['product_category'])['product_id'].value_counts()).rename({'product_id': 'purchase_count'}, axis = 1).reset_index().sort_values(by = 'purchase_count', ascending = False).reset_index(drop = True)

            return all_cluster[['product_category', 'product_id']].head(n_rec)

        elif cluster_name != 'all':
            
            df_cluster = df.loc[df['cluster_name'] == cluster_name]
            df_cluster = pd.DataFrame(df_cluster.groupby(['product_category'])['product_id'].value_counts()).rename({'product_id': 'purchase_count'}, axis = 1).reset_index().sort_values(by = 'purchase_count', ascending = False).reset_index(drop = True)
            
            return df_cluster[['product_category', 'product_id']].head(n_rec)


def main():
    
    df = load_data('df_rec_system.csv')

    st.title('Olist Recommendation System')

    menu = ['Home', 'Recommend', 'About']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader('Home')
        st.dataframe(df.head(10))

    if choice == 'Recommend':
        cluster_name = st.selectbox('Cluster Name', (['all'] +list(df['cluster_name'].unique())) , index = 0)
        state_name = st.selectbox('Customer State', (['all'] + list(df['customer_state'].unique())) , index = 0)
        n_rec = st.slider('Number of Product to Recommend', 10, 50)

        button = st.button('Recommend')

        if button:
            result = rec_system(df, cluster_name = cluster_name, customer_state = state_name, n_rec = n_rec)
            st.write(result)

    if choice == 'About':
        st.write('Recommendation System Built To Help Olist Store Marketing Team')


if __name__ == '__main__':
    main()