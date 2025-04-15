import streamlit as st
import pandas as pd
import csv
import time
import bcrypt
import ast


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
def chat():
  
  chat_page1 = st.Page(page="pages/chat.py", title="ChatBot")
  pg2 = st.navigation([chat_page1])
  pg2.run()

def login():

    from streamlit_option_menu import option_menu
 
        
    with st.sidebar:
      selected = option_menu(menu_title=None, options= ["Login", 'About','Chat'], 
      icons=['house', 'gear'], menu_icon="cast", default_index=0, orientation="vertical")
    
    if selected == "About":
     
      st.markdown("<h1 style='text-align: center; color: grey;'>Grocery Management System</h1>", unsafe_allow_html=True)
      st.divider()
      st.subheader(":violet[This management system will help you to add list of items to cart and export the added items to file for easy access.]")   
      
    if selected == "Chat":
      chat()
      
      

    if selected == "Login": 
      st.markdown("<h1 style='text-align: center; color: grey;'>Grocery Management System</h1>", unsafe_allow_html=True)
      st.divider()
      st.image("pages/image.png", caption="Grocery Management", use_container_width=True)
      
      with st.sidebar:
        
        tab1, tab2, tab3 = st.tabs(["Login", "Register", "Google Login"])

        with tab1:
          st.markdown("Login Screen", help="username and password are case sensitive")
          userid = st.text_input("Username", key="1")
          pwd = st.text_input("Password", type="password", key="2")
          
          
          if st.button("Login"):            
            
            is_found = False
            with open("useraccounts.csv", 'r') as file:
              reader = csv.reader(file)
              for item in reader:
                if userid in item:
                  is_found = True
                  df = pd.read_csv("useraccounts.csv",names=["username", "pass1"])
                  a1 = userid
                  idx = df[df["username"] == a1].index.tolist()

                  
                  get_pass = df._get_value(idx[0], "pass1")
                  #st.write("stored_hash:", get_pass)
                  
                  
                  stored_hash = ast.literal_eval(get_pass)
                  #stored_hash = get_pass.encode()
                  #stored_hash =get_pass.encode()
                  #st.write(stored_hash)


                  hashed2 = bcrypt.checkpw(pwd.encode(), stored_hash)
                  #st.write(hashed2)

                  if hashed2:
                    st.session_state.logged_in = True
                    st.success("Login Successful")
                    st.rerun()
                    
                    
                  else:
                    st.error("user id / password is invalid")
                    break
                  
              if is_found == False:
                st.error("User id not found")
              
        with tab2:
          
          userid1 = st.text_input("Username", key="3")
          
          pwd1 = st.text_input("Password", type="password", key="4")
          pwd_len = len(pwd1)

          hashed = bcrypt.hashpw(pwd1.encode(), bcrypt.gensalt())
          

          if st.button("Sign up"):
              if pwd_len < 5:
                st.info("Please choose password with min 5 characters")
              else:
                lines = open('useraccounts.csv', 'r').read()
                with open('useraccounts.csv','a+', newline='') as check:
                  if userid1 in lines:
                    with st.spinner("Please wait..."):
                      time.sleep(3)
                      st.error("Account already exists")
                  else:
                    wtr = csv.writer(check, delimiter= ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    wtr.writerow([userid1, hashed])
                    with st.spinner("Creating account..."):
                      time.sleep(3)
                      st.success("Account created")
                    #time.sleep(5)
                      st.rerun()
        with tab3:
          st.button(":rainbow[Login with google]", on_click=st.login, key=5, use_container_width=True,help="Click to login with your google account")
          
          if st.experimental_user.is_logged_in:
              st.session_state.logged_in = True

              st.success("Login Successful")
              st.rerun()

            
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background: rgba(10,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)
            


def logout():
    if st.button("Log out", on_click=st.logout):
        st.session_state.logged_in = False
        st.rerun()





  




login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

dashboard = st.Page(
    "pages/list.py", title="Dashboard", icon=":material/dashboard:", default=True
)





if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Reports": [dashboard],
            
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()