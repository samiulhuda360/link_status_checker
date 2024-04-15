def get_html_content_404(target_link, link_to, anchor_text):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Link Status Update</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 16px;
                background-color: #f7f7f7;
                padding: 20px;
                margin: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333333;
                font-size: 24px;
                margin-top: 0;
                margin-bottom: 20px;
                text-align: center;
                text-transform: uppercase;
                letter-spacing: 2px;
            }}
            p {{
                color: #555555;
                line-height: 1.6;
                margin-bottom: 15px;
            }}
            .error {{
                color: #ff3b30;
                font-weight: bold;
            }}
            .link-details {{
                margin-top: 30px;
                padding: 20px;
                background-color: #f2f2f2;
                border: 1px solid #dddddd;
                border-radius: 5px;
            }}
            .link-details p {{
                margin: 10px 0;
            }}
            .link-details strong {{
                color: #333333;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Link Status Update</h1>
            <p>Hi,</p>
            <p>We hope this email finds you well. We wanted to bring to your attention that the link we acquired from your website is currently showing a <span class="error">404 error</span>.</p>
            <div class="link-details">
                <p><strong>Backlink:</strong> {target_link}</p>
                <p><strong>Referring URL:</strong> {link_to}</p>
                <p><strong>Anchor Text:</strong> {anchor_text}</p>
            </div>
            <p>We kindly request your assistance in resolving this issue. Please review the link and take the necessary steps to ensure that it is functioning properly.</p>
            <p>If you have any questions or need further information, please don't hesitate to reach out to us. We appreciate your prompt attention to this matter.</p>
            <p>Thank you for your cooperation.</p>
            <br>
            <p>Best regards,</p>
            <p>Rohin<br>Seach Combat</p>

        </div>
    </body>
    </html>
    """
    
def get_html_content_link_removed(target_link, link_to, anchor_text):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Link Status Update</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 16px;
                background-color: #f7f7f7;
                padding: 20px;
                margin: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333333;
                font-size: 24px;
                margin-top: 0;
                margin-bottom: 20px;
                text-align: center;
                text-transform: uppercase;
                letter-spacing: 2px;
            }}
            p {{
                color: #555555;
                line-height: 1.6;
                margin-bottom: 15px;
            }}
            .removed {{
                color: #ff9900;
                font-weight: bold;
            }}
            .link-details {{
                margin-top: 30px;
                padding: 20px;
                background-color: #f2f2f2;
                border: 1px solid #dddddd;
                border-radius: 5px;
            }}
            .link-details p {{
                margin: 10px 0;
            }}
            .link-details strong {{
                color: #333333;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Link Status Update</h1>
            <p>Hi,</p>
            <p>We hope this email finds you well. We wanted to inform you that the link we acquired from your website has been <span class="removed">removed</span> from the referring URL.</p>
            <div class="link-details">
                <p><strong>Backlink:</strong> {target_link}</p>
                <p><strong>Referring URL:</strong> {link_to}</p>
                <p><strong>Anchor Text:</strong> {anchor_text}</p>
            </div>
            <p>We understand that websites undergo changes and updates, but we kindly request your assistance in restoring the link. The presence of the link is valuable to us, and we would greatly appreciate it if you could take the necessary steps to reinstate it.</p>
            <p>If there are any specific reasons for the link removal or if you have any concerns, please let us know. We are open to discussing any issues and finding a mutually beneficial solution.</p>
            <p>Thank you for your attention to this matter. We look forward to hearing back from you soon.</p>
            <p>Best regards,</p>
            <p>Rohin<br>Seach Combat</p>
        </div>
    </body>
    </html>
    """
    
def get_html_content_nofollow(target_link, link_to, anchor_text):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Link Status Update</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 16px;
                background-color: #f7f7f7;
                padding: 20px;
                margin: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333333;
                font-size: 24px;
                margin-top: 0;
                margin-bottom: 20px;
                text-align: center;
                text-transform: uppercase;
                letter-spacing: 2px;
            }}
            p {{
                color: #555555;
                line-height: 1.6;
                margin-bottom: 15px;
            }}
            .nofollow {{
                color: #ff6600;
                font-weight: bold;
            }}
            .link-details {{
                margin-top: 30px;
                padding: 20px;
                background-color: #f2f2f2;
                border: 1px solid #dddddd;
                border-radius: 5px;
            }}
            .link-details p {{
                margin: 10px 0;
            }}
            .link-details strong {{
                color: #333333;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Link Status Update</h1>
            <p>Hi,</p>
            <p>We hope this email finds you well. We wanted to bring to your attention that the link we acquired from your website is currently set to <span class="nofollow">"nofollow"</span> instead of "dofollow".</p>
            <div class="link-details">
                <p><strong>Backlink:</strong> {target_link}</p>
                <p><strong>Referring URL:</strong> {link_to}</p>
                <p><strong>Anchor Text:</strong> {anchor_text}</p>
            </div>
            <p>As you may know, having a "dofollow" link is valuable for SEO purposes as it passes link equity and helps improve search engine rankings. We kindly request your assistance in converting the link to "dofollow" status.</p>
            <p>If there are any specific reasons for using the "nofollow" attribute or if you have any concerns, please let us know. We would be happy to discuss further and address any questions you may have.</p>
            <p>Thank you for your attention to this matter. We look forward to your favorable response.</p>
            <br>
            <p>Best regards,</p>
            <p>Rohin<br>Seach Combat</p>

        </div>
    </body>
    </html>
    """