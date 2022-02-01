import sys

import pygame
import requests


def geo_search(search):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b" \
                       f"&geocode={search}&format=json"
    responses = requests.get(geocoder_request)
    if responses:
        json_response = responses.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # toponym_coodrinates = list(map(float, toponym["Point"]["pos"].split()))
        toponym_coodrinates = toponym["Point"]["pos"].replace(' ', ',')
        return toponym_coodrinates
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", responses.status_code, "(", responses.reason, ")")


def get_image(name):
    geos = list(map(float, geo_search(name).split(',')))
    geos[0] += move_x
    geos[1] += move_y
    geos = ','.join(list(map(str, geos)))
    response = requests.get(
        f"http://static-maps.yandex.ru/1.x/?ll={geos}&spn={scale},{scale}&l=map")

    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    return pygame.image.load(map_file)


def main(place):
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    pygame.display.set_caption('Слайд-шоу')
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(144)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.K_PAGEUP:
                print(111)
        screen.blit(get_image(place), (0, 0))
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    scale = 0.16
    move_x = 0
    move_y = 0
    main(['Санкт-Петербург'])
