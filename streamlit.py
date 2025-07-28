import streamlit as st


# -- Page Setup --

to_xendit = st.Page(
    'Menu/to_xendit.py',
    title = 'Cek ke Xendit',
)

to_midtrans = st.Page(
    'Menu/to_midtrans.py',
    title = 'Cek ke Midtrans',
)

#-- Navigation Setup [Without Sections] --
pg = st.navigation(pages = [to_xendit, to_midtrans])

# #-- Navigation Setup With Sections
# pg = st.navigation(
#     {
#         'Info' : [tentang_saya, homepage],
#         'Projects' : [project1_page, project2_page, dataset]
#     }
# )



# pages = {
#     'Info' : [
#         st.Page('Menu/tentang_saya.py', title='Tentang Saya')
#     ],
#     'Projects' : [
#         st.Page('Menu/dashboard.py', title='Dashboard')
#     ]
# }

# pg = st.navigation(pages)

#-- Run Navigation
pg.run()