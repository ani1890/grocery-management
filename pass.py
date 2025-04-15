from http import client
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import bcrypt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import time


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)
  
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
def chat():
  
  chat_page1 = st.Page(page="pages/chat.py", title="ChatBot")
  pg2 = st.navigation([chat_page1])
  pg2.run()



url = "https://docs.google.com/spreadsheets/d/1_Ur-XBJLPI8yaNB4BHP__68t-L0eUEPcHXV2uYXHkwE/edit?gid=0#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url, usecols=list(range(3)))

def login():

    from streamlit_option_menu import option_menu
    with st.sidebar:
      selected = option_menu(menu_title=None, options= ["Login", 'About','Chat'], 
      icons=['house', 'gear'], menu_icon="cast", default_index=0)
      
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
        
        tab1, tab2, tab3 = st.tabs(["Login", "Register", "Forgot Password"])

        with tab1:
          st.markdown("Login Screen", help="username and password are case sensitive")
              
          scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
          credentials_dict = st.secrets["service_account"]
          credentials = Credentials.from_service_account_info(credentials_dict, scopes=scope)
          
          client = gspread.authorize(credentials)

          sheet = client.open("user_account_grocery_app").sheet1
          userid = st.text_input("Username", key="1")
          pwd = st.text_input("Password", type="password", key="2")
          st.button(":rainbow[Login with google]", on_click=st.login, key=5,help="Click to login with your google account")
  
              if st.experimental_user.is_logged_in:
                  st.session_state.logged_in = True
    
                  st.success("Login Successful")
                  st.rerun()
      
          scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
          credentials_dict = st.secrets["service_account"]
          credentials = Credentials.from_service_account_info(credentials_dict, scopes=scope)
          
          client = gspread.authorize(credentials)
          new_value1 = pwd.encode('utf-8')
      
          if st.button("Login"):
                          
              if not userid or not pwd:
                st.warning("Ensure mandatory fields are filled.")
                
              else:
                
                all_data = sheet.get_all_values()
                row_number = None
                for idx, row in enumerate(all_data, start=1):  # start=1 because Google Sheets is 1-indexed
                    if userid in row:
                        row_number = idx
                        #st.write(f"Match found in row {row_number}:", row)
                        stored_hashed = row[1]

                        if bcrypt.checkpw(new_value1, stored_hashed.encode('utf-8')):
                          st.session_state.logged_in = True
                          with st.spinner("Verifying.."):
                            time.sleep(3)
                            st.success("Login successful")
                            st.rerun()
                        else:
                          st.error("Invalid Password")
        
                          break

                if row_number is None:
                    st.error("No user id found.")
                    
        with tab2:
           
            with st.spinner("Loading, Please wait....."):
              time.sleep(3)
              st.markdown("Enter new user details :")
            with st.form(key = "user_form"):
              username = st.text_input(label="Username*")
              password1 = st.text_input("Password*", type= "password")
              pwd_len = len(password1)

              hashed = hash_password(password1)
              hash_pwd = hashed.decode('utf-8')
              email_id = st.text_input("Email address")
              #st.write(data.columns)
              
              st.markdown(":red[**required*]")
    
              submit_button = st.form_submit_button(label="Sign up")
    
              if submit_button:
                
                if not username or not password1:
                  st.warning("Ensure mandatory fields are filled.")
                  data["UserName"] = data["UserName"].astype(str)
                elif data["UserName"].str.contains(username).any():
                  
                  st.warning("User Id already Exists.")
                else:
                                  user_data= pd.DataFrame(
                              [
                                  {
                                      "UserName": username,
                                      "Password": hash_pwd,
                                      "Email": email_id,
                                      
                                  }
                              ]
                          )
                                  updated_df = pd.concat([data, user_data], ignore_index=True)
                                  conn.update(spreadsheet=url, data=updated_df)
                                  with st.spinner("Creating user account..."):
                                    time.sleep(3)
                                    st.success("User id Created")
                                    st.rerun()
        with tab3:
          
          st.markdown("Enter existing user details :")
          with st.form(key = "forgot_password_form"):

          
            st.markdown(":red[**Mandatory*]")
    
    
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            credentials_dict = st.secrets["service_account"]
            credentials = Credentials.from_service_account_info(credentials_dict, scopes=scope)
            
            client = gspread.authorize(credentials)


        # Authorize client
            
            sheet = client.open("user_account_grocery_app").sheet1
            all_data = sheet.get_all_values()
            headers = all_data[0]  # First row is assumed to be the header
            data_rows = all_data[1:]
    
            column_name = st.selectbox("Need to update*", headers[1:], None)
            existing_username = st.text_input(label="Username*")
            new_pass = st.text_input("New Password*", type="password")
            confirm_pass = st.text_input("Confirm Password*", type="password")
            hashed = hash_password(new_pass)
            hash_pwd = hashed.decode('utf-8')
            confirm_email = st.text_input("Email address")
    
    
            if column_name == "Email":
              new_value = confirm_email
              
            elif column_name == "Password":
              new_value = hash_pwd
            
            change_pass = st.form_submit_button(label="Update Password")
            
            if not column_name or not existing_username or not new_pass or not confirm_pass:
                st.info("Ensure mandatory fields are filled.")
            
            if change_pass:
              found = False


              if column_name in headers:
                col_index = headers.index(column_name) + 1  # gspread is 1-indexed

                for idx, row in enumerate(data_rows):
                    if row[0] == existing_username:
                        row_number = idx + 2  # +2 because data starts at row 2
                        sheet.update_cell(row_number, col_index, new_value)
                        progress_bar = st.progress(0)

                        for percent_complete in range(100):
                            time.sleep(0.05)
                            progress_bar.progress(percent_complete + 1)
                        st.success("Password reset done")
                            #st.success(f"Updated '{column_name}' for '{existing_username}' in row {row_number}.")
                        found = True
                        break

              if not found:
                st.error("User id not found")
                    

              
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
          
          
                
                
#######################################################################################################################
