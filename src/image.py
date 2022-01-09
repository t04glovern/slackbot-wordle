from string import Template

from htmlwebshot import WebShot


def generate(event, context):
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
    filepath = "/tmp/wordle.svg"
    shot.create_pic(html=content.template, output=filepath)
    with open(filepath, "r") as file:
        image = file.read().replace("\n", "")

        return {
            "statusCode": 200,
            "body": image,
            "headers": {
                "Content-Type": "image/svg+xml",
            },
        }
