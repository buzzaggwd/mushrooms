import arcade

# Определяем все величины
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SPRITE_SCALING_PLAYER = 0.5
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 25
ENEMY_MOVEMENT_SPEED = 2
ENEMY_MOVEMENT_SPEED2 = 4
ENEMY_JUMP_SPEED = 10

# Создаем врагов и пули
class Enemy(arcade.Sprite):
    def __init__(self, image, scaling, center_x, center_y):
        super().__init__(image, scaling)
        self.center_x = center_x
        self.center_y = center_y
        self.change_x = ENEMY_MOVEMENT_SPEED

    def update(self):
        self.center_x += self.change_x
        if self.left < 260 or self.right > SCREEN_WIDTH*(2/3):
            self.change_x *= -1

class Enemy2(arcade.Sprite):
    def __init__(self, image, scaling, center_x, center_y):
        super().__init__(image, scaling)
        self.center_x = center_x
        self.center_y = center_y
        self.change_x = ENEMY_MOVEMENT_SPEED2

    def update(self):
        self.center_x += self.change_x
        if self.left < 0 or self.right > SCREEN_WIDTH:
            self.change_x *= -1


class Bullet(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        if self.top < 0:
            self.remove_from_sprite_lists()

# Окно1 (диалоговое)
class Window1(arcade.Window):
    def __init__(self):
        super().__init__(800, 500, "OK", resizable=True)
        # Цвет фона
        arcade.set_background_color(arcade.color.ASPARAGUS)
        # Создали кнопку
        self.button_width = 150
        self.button_height = 55
        self.button_x = 600
        self.button_y = 90

    #Здесь декоративная часть
    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "а мне лукошко с грибами\n важнее возможности заражения\n энцефалитной инфекцией и\n похищения гномами",
            self.width // 2,
            self.height // 2.5 + self.button_height + 10,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center",
            anchor_y="center",
            width=1200,
            align="center"
        )

        arcade.draw_rectangle_filled(
            self.button_x,
            self.button_y,
            self.button_width,
            self.button_height,
            arcade.color.ARMY_GREEN,
        )
        arcade.draw_text(
            "Погнали",
            self.button_x,
            self.button_y,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
        )

    # Делаем чтобы кнопка была рабочая
    def on_mouse_press(self, x, y, button, modifiers):
        if (
                self.button_x - self.button_width / 2 <= x <= self.button_x + self.button_width / 2
                and self.button_y - self.button_height / 2 <= y <= self.button_y + self.button_height / 2
        ):
            # Закрываем окно1 и открываем окно2
            self.close()
            window2 = Window2()
            window2.setup()
            arcade.set_window(window2)
            arcade.run()

    def setup(self):
        pass

# Окно2 (добрый лес)
class Window2(arcade.Window):
    # Блок Инит отвечает за основные настройки
    def __init__(self):
        # Вызываем окно
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "mushrooms")

        # Списки отслеживают спрайты, каждый спрайт идет в свой список
        self.wall_list = None
        self.player_list = None

        # Наш объект сцены
        self.scene = None

        # Этот список содержит спрайт игрока
        self.player_sprite = None

        # Наш физический движок
        self.physics_engine = None

        # Камера, которую можно использовать для прокрутки экрана
        self.camera = None

        # Загружаем фон картинкой
        self.background_textures = []
        for i in range(3):
            texture = arcade.load_texture("C:\\mushrooms\\добрый лес.jpg")
            self.background_textures.append(texture)

        self.background_width = self.background_textures[0].width
        self.background_height = self.background_textures[0].height
        self.background_left = 0
        self.background_bottom = 0

        # Делаем чтобы спрайты появлялись на экране
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()


    def on_close(self):
        # Закрываем окно2 и открываем окно3
        self.close()
        window3 = Window3()
        window3.setup()
        arcade.set_window(window3)
        arcade.run()

    # Блок Сетап это в основном настройки спрайтов
    def setup(self):
        # Устанавливаем камеру
        self.camera = arcade.Camera(self.width, self.height)

        # Инициализируем сцену
        self.scene = arcade.Scene()

        # Создаем списки спрайтов
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Размещаем персонажа
        image_source = "C:\\mushrooms\\бро1.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 180
        self.scene.add_sprite("Player", self.player_sprite)

        # Пол
        for x in range(0, 1600, 64):
            wall = arcade.Sprite("C:\\mushrooms\\добрая трава.jpg", TILE_SCALING)
            wall.center_x = x
            wall.center_y = -20
            self.scene.add_sprite("Walls", wall)

        # Основные спрайты
        # Платформы
        coordinate_list = [[500, 200], [700, 350], [350, 550], [150, 750], [1200, 850], [1450, 900], [1650, 950]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite("C:\\mushrooms\\добрая короткая платформа.png", TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        # Деревья
        coordinate_list3 = [[1500, 300], [1400, 200], [1300, 440], [850, 200]]
        for coordinate3 in coordinate_list3:
            wall = arcade.Sprite("C:\\mushrooms\\доброе дерево.png", TILE_SCALING)
            wall.position = coordinate3
            self.scene.add_sprite("Walls", wall)

        # Табличка
        coordinate_list3 = [[1200, 170]]
        for coordinate3 in coordinate_list3:
            wall = arcade.Sprite("C:\\mushrooms\\добрая табличка.png", TILE_SCALING)
            wall.position = coordinate3
            self.scene.add_sprite("Walls", wall)

        # Камни
        coordinate_list1 = [[1740, 200], [1700, 140], [1755, 160], [1720, 130], [1630, 130], [750, 130]]
        for coordinate1 in coordinate_list1:
            wall = arcade.Sprite("C:\\mushrooms\\добрый камень.png", TILE_SCALING)
            wall.position = coordinate1
            self.scene.add_sprite("Walls", wall)

        # Платформы2
        coordinate_list2 = [[450, 970], [800, 800], [2160, 950]]
        for coordinate2 in coordinate_list2:
            wall = arcade.Sprite("C:\\mushrooms\\добрая длинная платформа.png", TILE_SCALING)
            wall.position = coordinate2
            self.scene.add_sprite("Walls", wall)

        # Табличка2
        coordinate_list5 = [[3000, 500]]
        for coordinate5 in coordinate_list5:
            wall = arcade.Sprite("C:\\mushrooms\\табличка пока пока.png", TILE_SCALING)
            wall.position = coordinate5
            self.scene.add_sprite("Walls", wall)

        # Монеты
        for x in range(1000, 3000, 550):
            coin = arcade.Sprite("C:\\mushrooms\\грибмонетка.png", COIN_SCALING)
            coin.center_x = x
            coin.center_y = 1000
            self.scene.add_sprite("Coins", coin)

        # Создаем «физический движок»
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"])

    # Блок Дров отвечает за рендер
    def on_draw(self):

        # Очищаем экран
        self.clear()

        # Активируем камеру
        self.camera.use()

        # Рисуем фон
        for texture in self.background_textures:
            arcade.draw_texture_rectangle(self.background_left + texture.width / 2, self.background_bottom + texture.height / 2, texture.width, texture.height, texture)

        # Рисуем наши спрайты
        self.scene.draw()

    # Блоки, отвечающие за движок
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        # Не позволяет камере двигаться дальше 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        # Перемещает игрока с помощью физического движка
        self.physics_engine.update()

        # Размещаем камеру
        self.center_camera_to_player()

        # Монеты2
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()

# Окно3 (диалоговое)
class Window3(arcade.Window):
    def __init__(self):
        super().__init__(800, 500, "OK", resizable=True)
        arcade.set_background_color(arcade.color.ALABAMA_CRIMSON)

        self.button_width = 150
        self.button_height = 50
        self.button_x = 600
        self.button_y = 90

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Ой ой, ты упал в канаву. \n Кажется там что-то есть...",
            self.width // 2,
            self.height // 2 + self.button_height + 10,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center",
            anchor_y="center",
            width=1200,
            align="center"
        )

        arcade.draw_rectangle_filled(
            self.button_x,
            self.button_y,
            self.button_width,
            self.button_height,
            arcade.color.ALIZARIN_CRIMSON,
        )
        arcade.draw_text(
            "Что?",
            self.button_x,
            self.button_y,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
        )

    def on_mouse_press(self, x, y, button, modifiers):
        if (
                self.button_x - self.button_width / 2 <= x <= self.button_x + self.button_width / 2
                and self.button_y - self.button_height / 2 <= y <= self.button_y + self.button_height / 2
        ):
            # Close current window and open Window2
            self.close()
            window4 = Window4()
            window4.setup()
            arcade.set_window(window4)
            arcade.run()

    def setup(self):
        pass

# Окно4 (злой лес)
class Window4(arcade.Window):
    # Блок Инит отвечает за основные настройки
    def __init__(self):
        # Вызываем окно
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "mushrooms")

        # Списки отслеживают спрайты, каждый спрайт идет в свой список
        self.wall_list = None
        self.player_list = None

        # Наш объект сцены
        self.scene = None

        # Этот список содержит спрайт игрока
        self.player_sprite = None

        # Наш физический движок
        self.physics_engine = None

        # Камера, которую можно использовать для прокрутки экрана
        self.camera = None

        # Списки с врагами и пулями
        self.enemy_list = None
        self.enemy_list2 = None
        self.bullet_list = None

        # Загружаем фон картинкой
        self.background_textures = []
        for i in range(3):
            texture = arcade.load_texture(
                "C:\\mushrooms\\злой лес.jpg")
            self.background_textures.append(texture)

        self.background_width = self.background_textures[0].width
        self.background_height = self.background_textures[0].height
        self.background_left = 0
        self.background_bottom = 0

        # Эти штуки позволяют появляться спрайтам на экране
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

    # Блок Сетап это настройки спрайтов
    def setup(self):
        # Устанавливаем камеру
        self.camera = arcade.Camera(self.width, self.height)

        # Спрайты врагов и пуль
        self.enemy_list = arcade.SpriteList()
        self.enemy_list2 = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Инициализируем сцену
        self.scene = arcade.Scene()

        # Создаем списки спрайтов
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("Bullets")

        # Размещаем персонажа
        image_source = "C:\\mushrooms\\бро2.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 180
        self.scene.add_sprite("Player", self.player_sprite)

        # Создаем врагов
        enemy_sprite = Enemy("C:\\mushrooms\\монстр.png", CHARACTER_SCALING, 300, 760)
        self.enemy_list.append(enemy_sprite)

        enemy_sprite2 = Enemy2("C:\\mushrooms\\босс.png", CHARACTER_SCALING, 2000, 240)
        self.enemy_list2.append(enemy_sprite2)

        # Пол
        for x in range(0, 1800, 64):
            wall = arcade.Sprite("C:\\mushrooms\\злая трава.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = -20
            self.scene.add_sprite("Walls", wall)

        # Основные спрайты
        # Платформы
        coordinate_list = [[100, 500], [350, 350], [900, 750], [1200, 550]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite("C:\\mushrooms\\злая короткая платформа.png", TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        # Платформы2
        coordinate_list2 = [[650, 200], [500, 700], [1600, 650], [2000, 500]]
        for coordinate2 in coordinate_list2:
            wall = arcade.Sprite("C:\\mushrooms\\злая длинная платформа.png", TILE_SCALING)
            wall.position = coordinate2
            self.scene.add_sprite("Walls", wall)

        # Деревья
        coordinate_list3 = [[1350, 330]]
        for coordinate3 in coordinate_list3:
            wall = arcade.Sprite("C:\\mushrooms\\злое дерево.png", TILE_SCALING)
            wall.position = coordinate3
            self.scene.add_sprite("Walls", wall)

        # Камни
        coordinate_list1 = [[1700, 140], [1650, 120], [80, 120]]
        for coordinate1 in coordinate_list1:
            wall = arcade.Sprite("C:\\mushrooms\\злой камень1.png", TILE_SCALING)
            wall.position = coordinate1
            self.scene.add_sprite("Walls", wall)

        # Камни2
        coordinate_list1 = [[1210, 180]]
        for coordinate1 in coordinate_list1:
            wall = arcade.Sprite("C:\\mushrooms\\злой камень 2.png", TILE_SCALING)
            wall.position = coordinate1
            self.scene.add_sprite("Walls", wall)

        # Табличка
        coordinate_list4 = [[1600, 180]]
        for coordinate4 in coordinate_list4:
            wall = arcade.Sprite("C:\\mushrooms\\злая табличка.png", TILE_SCALING)
            wall.position = coordinate4
            self.scene.add_sprite("Walls", wall)

        # Создаем «физический движок»
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY,
                                                             walls=self.scene["Walls"])

    # Блок Дров отвечает за рендер
    def on_draw(self):
        # Очищаем экран
        self.clear()

        # Активируем камеру
        self.camera.use()

        # Рисуем фон
        for texture in self.background_textures:
            arcade.draw_texture_rectangle(self.background_left + texture.width / 2,
                                          self.background_bottom + texture.height / 2, texture.width, texture.height,
                                          texture)

        # Рисуем наши спрайты
        self.scene.draw()
        self.enemy_list.draw()
        self.enemy_list2.draw()
        self.bullet_list.draw()

    # Блоки, отвечающие за движок
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Создаем пули
        elif key == arcade.key.SPACE:
            bullet = Bullet("C:\\mushrooms\\зуб.png", CHARACTER_SCALING)
            bullet.center_x = self.player_sprite.center_x
            bullet.center_y = self.player_sprite.center_y*1.1
            bullet.change_x = 5
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        # Не позволяет камере двигаться дальше 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        # Перемещает игрока с помощью физического движка
        self.physics_engine.update()
        self.enemy_list.update()
        self.enemy_list2.update()
        self.bullet_list.update()

        # Логика врагов
        for enemy in self.enemy_list:
            if arcade.check_for_collision(self.player_sprite, enemy):
                arcade.close_window()  # Закрытие окна игры

        for enemy2 in self.enemy_list2:
            if arcade.check_for_collision(self.player_sprite, enemy2):
                arcade.close_window()  # Закрытие окна игры

        # Проверяем столкновение пуль с врагами
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()

        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list2)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for enemy2 in hit_list:
                    enemy2.remove_from_sprite_lists()

        # Размещаем камеру
        self.center_camera_to_player()

def main():
    window1 = Window1()
    window1.setup()
    arcade.set_window(window1)
    arcade.run()

if __name__ == "__main__":
    main()