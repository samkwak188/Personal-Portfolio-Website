import dash_mantine_components as dmc
from dash import Dash, html, dcc
from dash_iconify import DashIconify
from dash.dependencies import Input, Output, State

# Move this section to the top of the file, right after the imports
app = Dash(
    __name__,
    title="Sam Kwak - Portfolio"
)
app.config.suppress_callback_exceptions = True
server = app.server

# Update the card style
card_style = {
    "width": 400,
    "height": 400,
}

card1 = dmc.Card(
    children=[
        dmc.CardSection(
            dmc.Anchor(
                dmc.Image(
                    src="https://i.im.ge/2025/02/01/H24a1G.EPL.png",
                    alt="American Football Oracle GPT",
                ),
                href="https://epl-match-result-predictor-3.onrender.com",
                target="_blank"
            ),
        ),
        dmc.Group(
            [
                dmc.Text("EPL Match Result Predictor", weight=700, size='l'),
                html.A(
                    DashIconify(icon="ion:logo-github", width=30),
                    href='https://github.com/samkwak188/EPL-Match-Result-Predictor',
                    target="_blank"
                )
            ],
            position="apart",
            mt="md",
            mb="xs",
        ),
        dmc.Text(
            "A web application with a custom Machine Learning model that predict the outcome of EPL matches.",
            size="sm",
            color="dimmed",
        ),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style=card_style,
    className="card-hover",
)

card2 = dmc.Card(
    children=[
        dmc.CardSection(
            dmc.Anchor(
                dmc.Image(
                    src="https://i.im.ge/2025/02/01/H2GDUy.Youtube-shorts-Tiktok-video-generator-5.png",
                    alt="dash-app",
                ),
                href="https://www.youtube.com/watch?v=VhmSVoiDHdU",
                target="_blank"
            ),
        ),
        dmc.Group(
            [
                dmc.Text("Youtube shorts/ Tiktok video generator", weight=700, size='l'),
                html.A(
                    DashIconify(icon="ion:logo-github", width=30),
                    href='https://github.com/samkwak188/GoViral-Wizard---youtube-shorts-tiktok-video-creator',
                    target="_blank"
                )
            ],
            position="apart",
            mt="md",
            mb="xs",
        ),
        dmc.Text(
            "A free and easy to use that generates viral Youtube shorts/ Tiktok videos based on a text prompt.",
            size="sm",
            color="dimmed",
        ),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style=card_style,
    className="card-hover",
)

card3 = dmc.Card(
    children=[
        dmc.CardSection(
            dmc.Anchor(
                dmc.Image(
                    src="https://i.im.ge/2025/02/01/H2G7TJ.Youtube-shorts-Tiktok-video-generator-4.png",
                    alt="dash-app",
                ),
                href="https://my-service-662964498291.us-central1.run.app",
                target="_blank"
            ),
        ),
        dmc.Group(
            [
                dmc.Text("Fake text story video generator", weight=700, size='l'),
                html.A(
                    DashIconify(icon="ion:logo-github", width=30),
                    href='https://github.com/samkwak188/Fake-Text-Story-Video-Generator---Complete-Version',
                    target="_blank"
                )
            ],
            position="apart",
            mt="md",
            mb="xs",
        ),
        dmc.Text(
            "A web based video automation tool that generates trending fake text styled story videos.",
            size="sm",
            color="dimmed",
        ),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style=card_style,
    className="card-hover",
)

card4 = dmc.Card(
    children=[
        dmc.CardSection(
            dmc.Anchor(
                dmc.Image(
                    src="https://i.im.ge/2025/02/01/H248V1.generated-file-name.png",  # Placeholder image URL
                    alt="AI Face Type Analyzer",
                ),
                href="https://myfacetype.netlify.app",  # Placeholder link
                target="_blank"
            ),
        ),
        dmc.Group(
            [
                dmc.Text("AI Face Type Analyzer", weight=700, size='l'),
                html.A(
                    DashIconify(icon="ion:logo-github", width=30),
                    href='https://github.com/samkwak188/AI-Face-Type-Analyzer',  # Placeholder link
                    target="_blank"
                )
            ],
            position="apart",
            mt="md",
            mb="xs",
        ),
        dmc.Text(
            "A web application that analyzes the face type of uploaded image using a custom machine learning model trained with four categories of face type data.",
            size="sm",
            color="dimmed",
        ),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style=card_style,
    className="card-hover",
)

card5 = dmc.Card(
    children=[
        dmc.CardSection(
            dmc.Anchor(
                dmc.Image(
                    src="https://i.im.ge/2025/02/01/H2BXJF.3.png",  # Placeholder image URL
                    alt="Face detecting Image Crawler",
                ),
                href="https://github.com/samkwak188/Image-Crawler-with-Face-detection",
                target="_blank"
            ),
        ),
        dmc.Group(
            [
                dmc.Text("Face detecting Image Crawler", weight=700, size='l'),
                html.A(
                    DashIconify(icon="ion:logo-github", width=30),
                    href='https://github.com/samkwak188/Image-Crawler-with-Face-detection',  # Placeholder link
                    target="_blank"
                )
            ],
            position="apart",
            mt="md",
            mb="xs",
        ),
        dmc.Text(
            "Simple image crawling tool that crawl images of user specified keywords and detects faces in images and saves them to a local folder.",
            size="sm",
            color="dimmed",
        ),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style=card_style,
    className="card-hover",
)

engineering_card1 = html.Div(
    dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src="https://i.im.ge/2025/02/03/HdWsmz.prof-thumbnail-2.png",
                    alt="Kitchen Wastewater Purifier",
                ),
            ),
            dmc.Group(
                [
                    dmc.Text("Kitchen Wastewater Purifier", weight=700, size='l'),
                ],
                position="apart",
                mt="md",
                mb="xs",
            ),
            dmc.Text(
                "Built an working invention to address a real-life problem faced by most households and restaurants—kitchen wastewater. The invention features a mechanism that separates oil, odor, and food particles from kitchen wastewater, making the water reusable.",
                size="sm",
                color="dimmed",
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style=dict(card_style, cursor="pointer"),
        className="card-hover",
    ),
    id="engineering-card-1",
    n_clicks=0
)

engineering_card2 = html.Div(
    dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src="https://i.im.ge/2025/02/03/Hdkhza.prof-thumbnail-3.png",
                    alt="4D Movie Theater Headset",
                ),
            ),
            dmc.Group(
                [
                    dmc.Text("4D Movie Theater Headset", weight=700, size='l'),
                ],
                position="apart",
                mt="md",
                mb="xs",
            ),
            dmc.Text(
                "Developed an headset that shows movies with movie companion 4D effects that allows users to experience the movie in a more immersive way. "
                "C was used to code the whole system. Servo motors, water pumps, and mechanisms like crank and sliders were used. ",
                size="sm",
                color="dimmed",
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style=dict(card_style, cursor="pointer"),
        className="card-hover",
    ),
    id="engineering-card-2",
    n_clicks=0
)

engineering_card3 = html.Div(
    dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src="https://i.im.ge/2025/02/04/HqPpyL.prof-thumbnail-4.png",
                    alt="Dancing Humanoids",
                ),
            ),
            dmc.Group(
                [
                    dmc.Text("Dancing Humanoids", weight=700, size='l'),
                ],
                position="apart",
                mt="md",
                mb="xs",
            ),
            dmc.Text(
                "Built a humanoid robot and programmed it to dance to K-POP songs using C. Built the humanoids using servo motors and 3D printed parts. "
                "Performed at various local communites like churches during christmas and Holt School in Korea.",
                size="sm",
                color="dimmed",
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style=dict(card_style, cursor="pointer"),
        className="card-hover",
    ),
    id="engineering-card-3",
    n_clicks=0
)

all_cards = dmc.Tabs(
    [
        dmc.TabsList(
            [
                dmc.Tab("Coding Projects", value="coding"),
                dmc.Tab("Engineering Projects", value="engineering"),
            ],
            style={"marginBottom": 20}
        ),
        dmc.TabsPanel(
            dmc.SimpleGrid(
                cols=3,
                spacing="lg",
                breakpoints=[
                    {"maxWidth": 1240, "cols": 2, "spacing": "md"},
                    {"maxWidth": 950, "cols": 1, "spacing": "sm"},
                ],
                children=[
                    html.Div(card1),
                    html.Div(card2),
                    html.Div(card3),
                    html.Div(card4),
                    html.Div(card5),
                ],
            ),
            value="coding"
        ),
        dmc.TabsPanel(
            dmc.SimpleGrid(
                cols=3,
                spacing="lg",
                breakpoints=[
                    {"maxWidth": 1240, "cols": 2, "spacing": "md"},
                    {"maxWidth": 950, "cols": 1, "spacing": "sm"},
                ],
                children=[
                    html.Div(engineering_card1),
                    html.Div(engineering_card2),
                    html.Div(engineering_card3),
                ],
            ),
            value="engineering"
        )
    ],
    value="coding"
)

reference_card = html.Div([
    dmc.Card(
        children=[
            dmc.Text("Marge Simpson", weight=700, size='xl'),
            dmc.Text(
                "Pretzel business Owner",
                size="md",
                mb="xs",
            ),
            dmc.Text(
                "when a man's biggest dreams include seconds on dessert, occasional snuggling and sleeping in til noon on weekends, no one man can destroy them.",
                size="sm",
                color="dimmed",
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style=card_style,
        className="card-hover"
    )],
    style={"paddingTop": 40}
)

resume_div = html.Div([
    html.Iframe(src="https://docs.google.com/document/d/1MXY3hTm6kDqCytCHfL83_Ledi6Yakfk9/preview",
                width="800", height="480")
    ],
    style={"paddingTop": 40}
)

# Update the About Me tab content with a static globe design
about_content = html.Div([
    dmc.Stack(
        children=[
            dmc.Text("Hi, I'm Sam Kwak", weight=700, size='xl'),
            dmc.Text(
                "Full Stack Developer | Robotics Engineer",
                size="md",
                mb="xs",
            ),
            dmc.Text(
                "I'm a Full Stack Developer and Robotics Engineer passionate about building intelligent applications "
                "that solve real-world problems. With experience in Python and robotics, I specialize in creating "
                "practical software and hardwaretools for everyday use. My projects span various domains, from predictive analytics to automated "
                "content generation, all aimed at making complex technologies accessible and useful.\n\n"
                "In my work, I focus on developing solutions that are not only technically sound but also user-friendly and "
                "impactful. Whether it's software development or robotics, I strive to bridge the gap between advanced "
                "technology and practical applications.",
                size="sm",
                color="dimmed",
                mb="md",
            ),
            dmc.Group(
                [
                    html.A(
                        DashIconify(icon="skill-icons:linkedin", width=30),
                        href='https://www.linkedin.com/in/sam-kwak-0b9385314/',
                        target="_blank"
                    ),
                    html.A(
                        DashIconify(icon="ion:logo-github", width=30),
                        href='https://github.com/samkwak188',
                        target="_blank"
                    )
                ],
                spacing="lg",
            )
        ],
        spacing="sm",
        style={"maxWidth": 800, "padding": "20px"}  # Increased maxWidth since we removed the grid
    )
])

# Create modals for each engineering project
engineering_modal1 = dmc.Modal(
    title="Kitchen Wastewater Purifier",
    id="modal-1",
    size="70%",
    styles={
        "modal": {
            "maxHeight": "90vh",  # 90% of viewport height
        },
        "body": {
            "maxHeight": "calc(90vh - 80px)",  # Subtract header height
            "overflowY": "auto",  # Make content scrollable
            "paddingRight": "20px"  # Add some padding for the scrollbar
        }
    },
    children=[
        dmc.Image(
            src="https://i.im.ge/2025/02/03/HdWsmz.prof-thumbnail-2.png",
            width=800,
            mb="md",
        ),
        dmc.Text(
            "Detailed Project Description:",
            weight=700,
            size="lg",
            mb="sm",
        ),
        dmc.List([
            dmc.ListItem([
                dmc.Text("Problem:", weight=700),
                dmc.List([
                    dmc.ListItem("Kitchen wastewater from Malaysian households and restaurants contains high levels of oils and food particles, particularly from popular dishes like Laksa, Curry, Tanduri chicken and sambal sauce from Nasi Lemak."),
                    dmc.ListItem("Direct disposal into drains leads to sewer system damage, including clogging and unpleasant odors."),
                    dmc.ListItem("Current disposal methods result in significant water waste and increased utility costs."),
                ])
            ], mb="xl"),
            dmc.ListItem([
                dmc.Text("Solution:", weight=700),
                dmc.Text(
                    "Developed an innovative multi-stage filtration system that effectively processes and recycles kitchen wastewater.",
                )
            ], mb="xl"),
            dmc.ListItem([
                dmc.Text("Key Features:", weight=700),
                dmc.List([
                    dmc.ListItem("Advanced oil separation system utilizing density differences, integrated heating elements, and rotating oil scraping disks"),
                    dmc.ListItem("Dual-layer odor elimination system combining activated carbon and zeolite filtration"),
                    dmc.ListItem("Comprehensive particle filtration system for removing food residue"),
                ])
            ], mb="xl"),
            dmc.ListItem([
                dmc.Text("Impact:", weight=700),
                dmc.List([
                    dmc.ListItem("Environmental: Significantly reduces water waste through efficient recycling"),
                    dmc.ListItem("Financial: Lowers water utility costs for businesses and households"),
                    dmc.ListItem("Infrastructure: Prevents sewer system damage and reduces maintenance costs"),
                ])
            ]),
        ]),
    ],
)

engineering_modal2 = dmc.Modal(
    title="4D Movie Theater Headset",
    id="modal-2",
    size="70%",
    styles={
        "modal": {
            "maxHeight": "90vh",
        },
        "body": {
            "maxHeight": "calc(90vh - 80px)",
            "overflowY": "auto",
            "paddingRight": "20px"
        }
    },
    children=[
        dmc.Image(
            src="https://i.im.ge/2025/02/03/Hdkhza.prof-thumbnail-3.png",
            width=800,
            mb="md",
        ),
        dmc.Text(
            "Detailed Project Description:",
            weight=700,
            size="lg",
            mb="sm",
        ),
        dmc.List([
            dmc.ListItem([
                dmc.Text("Achievement:", weight=700),
                dmc.Text(
                    "First place winner in World Robot Olympiad Korea (In my age category)",
                )
            ], mb="xl"),
            dmc.ListItem([
                dmc.Text("Motivation:", weight=700),
                dmc.Text(
                    "Inspired by a childhood friend with mobility disabilities who struggled to access cinema facilities. "
                    "Created this solution with my ArtRobot Robotics team to bring an enhanced movie experience to those who face challenges visiting traditional theaters, "
                    "offering not just accessibility but an improved experience with 4D effects that surpass standard cinema offerings."
                )
            ], mb="xl"),
            dmc.ListItem([
                dmc.Text("Technology Stack:", weight=700),
                dmc.List([
                    dmc.ListItem("C programming for system control and effect synchronization"),
                    dmc.ListItem("Custom-designed hardware integration combining 3D printed components with motorcycle helmet base"),
                    dmc.ListItem("Mechanical assembly using acrylic boards, motors, pumps, and specialized tubing"),
                ])
            ], mb="xl"),
            dmc.ListItem([
                dmc.Text("4D Effects Implementation:", weight=700),
                dmc.List([
                    dmc.ListItem("Rain simulation using strategically placed water pumps and spray systems"),
                    dmc.ListItem("Motion effects through servo motors with crank and slider mechanisms"),
                    dmc.ListItem("Atmospheric effects including scent diffusion and mist generation"),
                    dmc.ListItem("Dynamic lighting system synchronized with movie scenes"),
                    dmc.ListItem("Real-time effect synchronization with movie timestamps"),
                ])
            ], mb="xl"),
            dmc.ListItem([
                dmc.Text("Impact:", weight=700),
                dmc.List([
                    dmc.ListItem("Accessibility: Brings immersive movie experiences to people with mobility challenges"),
                    dmc.ListItem("Innovation: Combines multiple sensory effects for a more engaging experience than traditional theaters"),
                    dmc.ListItem("Recognition: Project's success demonstrated by winning first place in WRO Korea"),
                ])
            ]),
        ]),
    ],
)

engineering_modal3 = dmc.Modal(
    title="Dancing Humanoids",
    id="modal-3",
    size="70%",
    styles={
        "modal": {
            "maxHeight": "90vh",
        },
        "body": {
            "maxHeight": "calc(90vh - 80px)",
            "overflowY": "auto",
            "paddingRight": "20px"
        }
    },
    children=[
        dmc.Image(
            src="https://i.im.ge/2025/02/04/HqPpyL.prof-thumbnail-4.png",
            width=800,
            mb="md",
        ),
        dmc.Text(
            "Detailed Project Description:",
            weight=700,
            size="lg",
            mb="sm",
        ),
        dmc.List([
            dmc.ListItem([
                dmc.Text("Technical Implementation:", weight=700),
                dmc.List([
                    dmc.ListItem("Multi-servo motor system controlling arms, legs, and head movements"),
                    dmc.ListItem("Custom C programming for choreographed dance sequences"),
                    dmc.ListItem("Synchronized movement patterns designed for popular K-pop songs"),
                ])
            ], mb="xl"),
            dmc.ListItem([
                dmc.Text("Community Impact:", weight=700),
                dmc.List([
                    dmc.ListItem("Chung-Jung Church Christmas Event:", [
                        dmc.List([
                            dmc.ListItem("Coordinated performance featuring 5 synchronized humanoid robots"),
                            dmc.ListItem("Special entertainment program designed for children under 12"),
                        ])
                    ]),
                    dmc.ListItem("Holt School & Disabled Welfare Center:", [
                        dmc.List([
                            dmc.ListItem("Live demonstration of robotic technology through dance performances"),
                            dmc.ListItem("Interactive showcase promoting STEM education and robotics awareness"),
                        ])
                    ]),
                ])
            ], mb="xl"),
            dmc.ListItem([
                dmc.Text("Project Outcomes:", weight=700),
                dmc.List([
                    dmc.ListItem("Educational: Demonstrated practical applications of robotics and programming to students"),
                    dmc.ListItem("Entertainment: Created engaging performances that combine technology with artistic expression"),
                    dmc.ListItem("Community Service: Brought innovative technology demonstrations to diverse community groups"),
                ])
            ]),
        ]),
    ],
)

# Then place the callbacks after all components are defined but before the layout
@app.callback(
    Output("modal-1", "opened"),
    Input("engineering-card-1", "n_clicks"),
    State("modal-1", "opened"),
    prevent_initial_call=True,
)
def toggle_modal1(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output("modal-2", "opened"),
    Input("engineering-card-2", "n_clicks"),
    State("modal-2", "opened"),
    prevent_initial_call=True,
)
def toggle_modal2(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output("modal-3", "opened"),
    Input("engineering-card-3", "n_clicks"),
    State("modal-3", "opened"),
    prevent_initial_call=True,
)
def toggle_modal3(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Finally, define the layout
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    withGlobalStyles=True,
    children=[
        engineering_modal1,
        engineering_modal2,
        engineering_modal3,
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.Tab("About Me", value="about"),
                        dmc.Tab("Projects", value="projects"),
                        dmc.Tab("Resumé", value="resume"),
                    ], 
                    style={"paddingRight": 50, "paddingTop": 15}
                ),
                dmc.TabsPanel(
                    about_content,
                    value="about",
                    pb="xs"
                ),
                dmc.TabsPanel(
                    html.Div([
                        dmc.Header(
                            height=80,
                            children=[dmc.Text("My Projects", style={"fontSize": 40})],
                        ),
                        all_cards
                    ]),
                    value="projects",
                    pb="xs"
                ),
                dmc.TabsPanel(resume_div, value="resume", pb="xs"),
            ],
            value="about",
            orientation='vertical',
            variant='pills',
        )
    ]
)

if __name__=='__main__':
    app.run(debug=False)