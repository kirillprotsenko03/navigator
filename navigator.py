import pygame
import sys
import math



# name of game
TITLE = 'navigator'

# size of screen
HEIGHT, WIDTH = 800, 1200

# colors  in RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# radius of circle
RADIUS = 5


class Station:
      """ draw station on screen, have a distanse between another stations
          and this station if they have connection."""

      def __init__(self, screen, x: int, y: int, station_id: int) -> None:
            self.screen = screen
            self.color = GREEN
            self.radius = RADIUS  # the radius of circle around station
            # coordinates of station
            self.x = x  
            self.y = y
            # number of emergence on the screen
            self.station_id = station_id

      def get_x(self) -> int:
            return self.x

      def get_y(self) -> int:
            return self.y

      def get_radius(self) -> int:
            return self.radius

      def get_id(self) -> int:
            return self.station_id

      def change_color(self, color) -> None:
            self.color = color

      def draw(self) -> None:
            pygame.draw.circle(self.screen, self.color,
                               (self.x, self.y), self.radius)


class Map:
      """ TODO: need to come up with description of this class!!!"""

      def __init__(self, screen) -> None:
            self.screen = screen
            self.stations = {} # {int id_station: class Station}
            self.stations_connect = {}  # {int id_station: list connected_station}
            self.count_station = 0

      def _get_distance(self, first_id: int, second_id: int) -> float:
            """return distance between two stations """
            if first_id == second_id:
                  return math.inf
            if first_id not in self.stations_connect or second_id not in self.stations_connect:
                  return math.inf
            if second_id not in self.stations_connect[first_id]:
                  return math.inf
            first_station = self.stations[first_id]
            second_station = self.stations[second_id]
            x1 = first_station.get_x()
            y1 = first_station.get_y()
            x2 = second_station.get_x()
            y2 = second_station.get_y()
            distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)  # just theorem of Pythagoras
            return distance

      def dijkstra(self, first_id: int, second_id: int) -> list:
            d = {i+1: [math.inf, 0] for i in range(len(self.stations))}
            d[first_id] = [0, first_id]
            seen = []
            for _ in range(len(self.stations)):
                  # find smallest distance
                  m = math.inf
                  for station in d:
                        if d[station][0] <= m and station not in seen:
                              w = station
                              m = d[station][0]
                  seen.append(w)
                  # find distance from this station to anothers
                  way_before = d[w][0]
                  for station in d:
                        distance = self._get_distance(w, station) + way_before
                        if distance < d[station][0]:
                              d[station][0] = distance
                              d[station][1] = w
            res = []
            a = second_id
            while a != first_id:
                  res.append(a)
                  a = d[a][1]
            res.append(first_id)
            return res[::-1]
                              
      def get_stations(self) -> dict:
            return self.stations

      def get_stations_connect(self) -> dict:
            return self.stations_connect

      def add_station(self, x: int, y: int) -> None:
            self.count_station += 1
            new_id = self.count_station
            station = Station(self.screen, x, y, new_id)
            self.stations[new_id] = station

      def add_connection_station(self, first_id: int, second_id: int) -> None:
            if first_id != second_id:
                  if first_id not in self.stations_connect:
                        self.stations_connect[first_id] = []
                  if second_id not in self.stations_connect:
                        self.stations_connect[second_id] = []
                  if second_id not in self.stations_connect[first_id]:
                        self.stations_connect[first_id].append(second_id)
                  if first_id not in self.stations_connect[second_id]:
                        self.stations_connect[second_id].append(first_id)


def in_circle(x: int, y: int, x_circle, y_circle, radius) -> bool:
      """ function just define if (x, y) in circle"""
      if math.sqrt((x - x_circle) ** 2 + (y - y_circle) ** 2) > radius:
            return False
      return True
      

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption(TITLE)
city_map = Map(screen)
game_mode = 'adding'
game_modes = ['connecting', 'finding', 'adding']
choosen_station = False

while True:
      # handling of game events
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  sys.exit()
            # there are 3 modes of game:
            # adding and delliting station, connecting stations, finding shortest way
            if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_SPACE:
                        game_mode = game_modes.pop(0)
                        game_modes.append(game_mode)
                        choosen_station = False
                        
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                  x = event.pos[0]  # coord x of mouse when it was pressed
                  y = event.pos[1]  # coord y of mouse when it was pressed
                  id_station = False  # if (x, y) of mouse in circle: id_station = Station.id_station
                  for station in city_map.get_stations().values():
                        x_circle = station.get_x()
                        y_circle = station.get_y()
                        radius = station.get_radius()
                        if in_circle(x, y, x_circle, y_circle, radius):
                              id_station = station.get_id()
                              
                  if id_station:  # if you click to circle. id_station is id of circle you click
                        if not choosen_station:
                              choosen_station = id_station
                        else:
                              first_id = choosen_station
                              second_id = id_station
                              if game_mode == 'connecting':
                                    city_map.add_connection_station(first_id, second_id)
                              if game_mode == 'finding':
                                    path = city_map.dijkstra(first_id, second_id)
                                    for station in city_map.get_stations().values():
                                          if station.get_id() in path:
                                                station.change_color(RED)
                              choosen_station = False
                        
                  else:
                        if game_mode == 'adding':
                              city_map.add_station(x, y)



      # draw all elements of game
      screen.fill(BLACK)
      stations = city_map.get_stations()
      connected_station = city_map.get_stations_connect()
      for station in stations.values():
            station.draw()

      # draw lines between connected stations
      for station in connected_station:
            start_s = stations[station]
            start_x = start_s.get_x()
            start_y = start_s.get_y()
            for end_s in connected_station[station]:
                  end_x = stations[end_s].get_x()
                  end_y = stations[end_s].get_y()
                  pygame.draw.line(screen, WHITE, (start_x, start_y), (end_x, end_y))

      # update screen
      pygame.display.update()

