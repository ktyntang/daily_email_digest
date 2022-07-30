import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests                 # download html
from bs4 import BeautifulSoup   # get data from html

links = []
subtext = []
for page_no in range(1,3):
    res = requests.get('https://news.ycombinator.com/news?p='+ str(page_no))
    soup = BeautifulSoup(res.text, 'html.parser')
    links.append(soup.select('.titlelink'))
    subtext.append(soup.select('.subtext'))

def custom_hn(links, subtext):
    hn = []
    for n, link in enumerate(links[0]):
        title = link.getText()
        href = link.get('href', None)
        vote = subtext[0][n].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points',''))
            if points >= 100:
                hn.append([points,title,href])
    return hn

def sort_by_points(hnlist):
    return sorted(hnlist, reverse= True)

def save_html(content):
    data = ""
    for l in content:
        data += "<td>" + str(l[0]) + "</td>"
        data += "<td>" + '<a href=+' + str(l[2]) + '>' + str(l[1]) + '</a>' + "</td>"
        data += "<tr>"
    data = "<table border=1>" + data + "<table>"

    with open("file.html", "w") as file:
        file.write(data)

def email_daily():
    html_file = open("file.html", "r")
    content = html_file.read()

    email = MIMEMultipart()
    email['from'] = 'K-Tyn Tang'
    email['to'] = 'ktyntang@hotmail.com'
    email['subject'] = 'HN updates!'

    email.attach(MIMEText(content, "html"))

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('ktyntang@gmail.com','app_password')
        smtp.send_message(email)
        print('sent!')

def app():
    save_html((sort_by_points(custom_hn(links, subtext))))
    email_daily()

if __name__ == '__main__':
    app()
