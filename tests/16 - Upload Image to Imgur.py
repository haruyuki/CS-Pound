import webbrowser
import pyimgur


CLIENT_ID = '7764ba66fbf9523'
CLIENT_SECRET = 'b6b1e0557c79baa75fc144f81447dacf01f45b98'
PATH = 'file.png'

im = pyimgur.Imgur(CLIENT_ID, client_secret=CLIENT_SECRET, access_token='fc5c0ffccff4387cef948df004edb1411575eaac', refresh_token='54b539be920b6327b31537ea7ad2514093a5c661')
uploaded_image = im.upload_image(path=PATH, title='file2', description='Testing', album='BiVzx')
print(uploaded_image.title)
print(uploaded_image.link)
print(uploaded_image.size)
print(uploaded_image.type)