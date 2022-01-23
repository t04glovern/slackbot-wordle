import base64
from string import Template

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from htmlwebshot import WebShot

logger = Logger(service="image")

@logger.inject_lambda_context
def generate(event, context: LambdaContext):
    shot = WebShot()
    shot.size = (248, 236)

    content = Template(
        """
    <!DOCTYPE html>
    <html>

    <head>
        <title></title>
        <meta charset="UTF-8">
        <style>
            .wordle td {
                border: 3px solid #d3d6da;
                width: 40px;
                height: 40px;
                text-align: center;
                font-size: 32px;
                font-weight: 700;
                line-height: 0;
                font-family: 'Clear Sans', 'Helvetica Neue', Arial, sans-serif;
            }

            .wordle .correct {
                background: #6aaa64;
                border: 0px;
                color: #ffffff;
            }

            .wordle .absent {
                background: #787c7e;
                border: 0px;
                color: #ffffff;
            }

            .wordle .present {
                background: #c9b458;
                border: 0px;
                color: #ffffff;
            }

            .wordle .empty {
                background: #ffffff;
            }
        </style>
    </head>

    <body>
        <table class="wordle">
            <tbody>
                <tr>
                    <td class="absent">A</td>
                    <td class="present">R</td>
                    <td class="present">O</td>
                    <td class="absent">S</td>
                    <td class="correct">E</td>
                </tr>
                <tr>
                    <td class="absent">F</td>
                    <td class="present">R</td>
                    <td class="present">O</td>
                    <td class="correct">G</td>
                    <td class="absent">S</td>
                </tr>
                <tr>
                    <td class="empty"></td>
                    <td class="empty"></td>
                    <td class="empty"></td>
                    <td class="empty"></td>
                    <td class="empty"></td>
                </tr>
                <tr>
                    <td class="empty"></td>
                    <td class="empty"></td>
                    <td class="empty"></td>
                    <td class="empty"></td>
                    <td class="empty"></td>
                </tr>
                <tr>
                    <td class="empty"></td>
                    <td class="empty"></td>
                    <td class="empty"></td>
                    <td class="empty"></td>
                    <td class="empty"></td>
                </tr>
            </tbody>
        </table>
    </body>

    </html>
    """
    )
    htmlpath = "/tmp/wordle.html"
    with open(htmlpath, "w") as htmlfile:
        htmlfile.write(content.template)

    pngpath = "/tmp/wordle.png"
    imagefile = shot.create_pic(html=htmlpath, output=pngpath)
    with open(imagefile, "rb") as file:
        image = base64.b64encode(file.read()).decode('utf-8')

    return {
        "statusCode": 200,
        "body": image,
        "isBase64Encoded": "true",
        "headers": {
            "Content-Type": "image/png",
        },
    }
