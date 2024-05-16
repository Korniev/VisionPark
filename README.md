<a name="readme-top"></a>
<br />
<div align="center">
  <h3 align="center">VISION PARK</h3>

  <p align="center">
    Parking management system based on computer vision model made by VisionPark Team
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li><a href="#contributors">Contributors</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot](https://github.com/Korniev/VisionPark/blob/main/vision_park/vision_park/static/img/main_screen.png)

Vision Park "ACE OF BASE" is a web app parking management system based on computer vision model which has next implemented features:
* Registration
* Login
* Car's plate number recognition
* Payment
* Profile information
* Parking area visualisation
* Download CSV analytics
* Telegram bot

We have developed a web application that can automatically identify license plate numbers in images, track the duration of parking for each unique vehicle, and calculate accumulated parking costs.
The web service was developed on the basis of the Django framework, the computer vision model was implemented using OpenCV, a Postgres database for permanent storage of license plates and data, and the creation of a Docker image that would allow us to host and run our application in a containerized environment.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With


* ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
* ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
* ![Docker](https://img.shields.io/badge/docker-blue?style=for-the-badge&logo=docker&logoColor=white)
* ![YOLOv5](https://img.shields.io/badge/yolov5-orange?style=for-the-badge&logo=yolov5&logoColor=white)
* ![JavaScript](https://img.shields.io/badge/javascript-yellow?style=for-the-badge&logo=javascript&logoColor=white)
* ![Bootstrap](https://img.shields.io/badge/bootstrap-purple?style=for-the-badge&logo=bootstrap&logoColor=white)
* ![HTML](https://img.shields.io/badge/html-orange?style=for-the-badge&logo=html5&logoColor=white)
* ![CSS](https://img.shields.io/badge/css-purple?style=for-the-badge&logo=css3&logoColor=white)


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get installed our web app you should follow these simple steps:


1. Clone the repository:

```bash
https://github.com/Korniev/VisionPark
```
2. Change to the project's directory:
```bash
cd VisionPark
```

3. You can make a docker compose for easy use of our application. You should write a following command in the terminal:

```bash
docker compose up --build
```

4. Now you can go to your browser and tap:

```bash
http://0.0.0.0:8000
```

5. To stop running docker compose you shoud write next command in terminal:

```bash
docker compose stop
```

6. To remove docker compose you should write next command in terminal:

```bash
docker compose down
```

We hope you enjoy our web application! :)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contributors

Project made by Vision Park Team:
* [Korniev](https://github.com/Korniev)
* [JuliManhupli](https://github.com/JuliManhupli)
* [Maximus-22](https://github.com/Maximus-22)
* [Almixs](https://github.com/Almixs)
* [Roman-K26](https://github.com/Roman-K26)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

