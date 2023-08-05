# ============== yodine_data ==============
#             by Gustavo6046
# licensed under MIT
#
#   All the assets, entities and levels that come with Yodine (the game). Note there can be multiple games for Yodine (the engine).

# This is the main code of your plugin.
# Here you will add all of the logic that will
# be used by your plugin.

# The lines below import all of the classes you'll
# use from Yodine.
from yodine.core.entity import EntityTemplate, Entity, System, TileType, Component, EventContext
from yodine.core.extension import ModLoader
from yodine.core.vector import ComponentVector, Vector
from yodine.game import Game

# Other imports go below.
import os
import pyglet
import math

from pyglet.window import key
from .inventory import ItemContainer

try:
    import simplejson as json

except ImportError:
    import json



DEFAULT_WEIGHT = 100

# Defines an extra resource path.
pyglet.resource.path.append(os.path.join(os.path.split(__file__)[0], 'assets'))
pyglet.resource.reindex()


# These helper functions will access assets for you :)
def asset_path(asset_name: str) -> str:
    return os.path.join(os.path.split(__file__)[0], 'assets', asset_name)


def open_asset(asset_name: str):
    return open(asset_path(asset_name))


# This function will be called when the plugin is
# loaded.
def loaded(loader: ModLoader):
    # === Routines ===

    def get_pos(entity: Entity, component_name: str = 'position') -> ComponentVector:
        assert component_name in entity
        return ComponentVector(entity[component_name])

    # Defines a standard tile type (background - does nothing).
    class FloorTileType(TileType):
        name = 'floor'

    # Defines a custom tile type (foreground - e.g. collides).
    class WallTileType(TileType):
        name = 'wall'
        post = True

        def collides(self, manager: 'Manager', ent: 'Entity', x, y) -> bool:
            if 'position' not in ent:
                return (None, 0, 0)

            if 'bounding_box' not in ent:
                ent['bounding_box'] = [25, 25]

            box = ComponentVector(ent['bounding_box'])
            pos = ComponentVector(ent['position'])

            dx = pos.x - x * 35 - 35 / 2
            dy = pos.y - y * 35 - 35 / 2

            rx = math.copysign(35 - abs(dx), dx)
            ry = math.copysign(35 - abs(dy), dy)

            collision = (
                abs(dx) <= box.x / 2 + 35 / 2 and
                abs(dy) <= box.y / 2 + 35 / 2
            )

            if collision:
                if abs(dx) > abs(dy):
                    return "horizontal", rx, ry

                else:
                    return "vertical", rx, ry

            return (None, 0, 0)

        def on_move(self, event: EventContext, start_pos):
            entity = event.source
            manager = event.manager

            if 'position' not in entity:
                return

            p = ComponentVector(entity['position'])

            for ((x, y), tt) in manager.current_level.tiles.items():
                if tt == self.name:
                    col, rx, ry = self.collides(manager, entity, x, y)

                    if col:
                        if 'velocity' in entity:
                            vel = ComponentVector(entity['velocity'])

                            if col == 'horizontal':
                                vel.x *= -0.5

                            else:
                                vel.y *= -0.5

                            if col == 'horizontal':
                                p.x += rx

                            else:
                                p.y += ry

                        manager.emit(entity, 'hit_wall', col)

    loader.add_tile_type(WallTileType(pyglet.resource.image('tiles/wall.png'), 'wall'))
    loader.add_tile_type(WallTileType(pyglet.resource.image('tiles/metal-wall.png'), 'mtlwall'))
    loader.add_tile_type(FloorTileType(pyglet.resource.image('tiles/floor.png'), 'floor'))
    loader.add_tile_type(FloorTileType(pyglet.resource.image('tiles/stone-floor.png'), 'stnfloor'))
    loader.add_tile_type(FloorTileType(pyglet.resource.image('tiles/dirt-floor.png'), 'dirt'))
    loader.add_tile_type(FloorTileType(pyglet.resource.image('tiles/metal-floor.png'), 'mtlfloor'))
    loader.add_tile_type(FloorTileType(pyglet.resource.image('tiles/ice.png'), 'ice'))

    # Defines a routine, which may be used by this or other
    # plugins.
    @loader.routine('init.game')
    def yodine_init(game: Game):
        # Routines can be accessed like a dict to
        # obtain all routines in a group (and its
        # subgroups), and those can also be accessed
        # via attributes directly by their name.
        for rout in loader.routines['init.yodine']:
            rout(game)

    # -> Level Definitions
    @loader.routine('init.yodine')
    def start_level(game: Game):
        manag = game.manager

        start_level = manag.create_level('start')
        start_level.rectangle(Vector((-20, -20)), 40, 40, 'floor')

        start_level.rectangle(Vector((-21, -21)), 1, 42, 'wall')
        start_level.rectangle(Vector((20, -21)), 1, 42, 'wall')

        start_level.rectangle(Vector((-20, 20)), 41, 1, 'wall')
        start_level.rectangle(Vector((-20, -21)), 41, 1, 'wall')

        manag.change_level('start')

        return start_level

    @loader.routine('init.yodine')
    def fps_counter(game: Game):
        game.manager.current_level.create_templated_entity('fpscounter')

    @loader.routine('init.player')
    def add_player(game: Game):
        player = game.manager.current_level.create_templated_entity('player', [
            ('localplayer', game.id),
            ('name', game.player_name),
        ])
        return player

    # === Systems ===

    # Defines a system to be registered by
    # the loader.

    @loader.system_type
    class S_LabelRender(System):
        component_types = ['name', 'position']

        def render(self, entity: Entity, window: pyglet.window.Window, name, position, *args, **kwargs) -> None:
            pos = get_pos(entity)
            x, y = self.manager.camera_transform(window, *pos)
            y += 75

            label = pyglet.text.Label(
                name.value,
                anchor_x = 'center',
                anchor_y = 'center',
                align='center',
                x = x,
                y = y,
                bold = True,
                font_size=18 * self.manager.camera_zoom
            )
            label.draw()


    @loader.system_type
    class S_FPSCounter(System):
        component_types = ['fpscounter']

        def render(self, entity: Entity, window: pyglet.window.Window, *args, **kwargs) -> None:
            if hasattr(self, 'dtime'):
                label = pyglet.text.Label(
                    str(round(1 / self.dtime, 1)),
                    x = 30,
                    y = 30,
                    bold = True
                )
                label.draw()

        def tick(self, entity: Entity, dtime: float, *args, **kwargs):
            self.dtime = dtime


    @loader.system_type
    class S_Velocity(System):
        component_types = ['position', 'velocity']
        component_defaults = {'friction': 0.425}

        def tick(self, entity: Entity, dtime: float, position, velocity, friction):
            vel = ComponentVector(velocity)

            if vel.sqsize() > 0.05 ** 2:
                pos = ComponentVector(position)
                oldpos = Vector(pos)
                pos += vel * dtime

                self.manager.emit(entity, 'move', oldpos)
                vel /= (1 + friction.value) ** dtime

    # Defines an entity template, a way to specify how certian
    # entities should be created.
    @loader.template
    class T_Player(EntityTemplate):
        # The name of this template. Used when looking it up.
        name = 'player'

        # The group of this template. Used when looking a specific group of templates up.
        group = 'living'

        # A list of default components.
        default_components = [
            ('name', 'a nameless player'),
            ('life', 100.0),
            ('position', [0, 0], 'VectorComponent'),
            ('angle', 0),
            ('velocity', [0, 0], 'VectorComponent'),
            ('player_move',),
            ('toward', [0, 0], 'VectorComponent'),
            ('speed', 200),
            ('inventory', {}, 'InventoryComponent'),
            ('player',),
            ('bounding_box', (20, 20), 'VectorComponent'),
            ('render', 'normal'),
            ('sprite', 'player'),
            ('pushable',),
            ('weight', 100),
            ('collides',),
        ]

    
    @loader.template
    class T_AIPlayer(EntityTemplate):
        editor_visible = True

        # The name of this template. Used when looking it up.
        name = 'bot'

        # The group of this template. Used when looking a specific group of templates up.
        group = 'living'

        # A list of default components.
        default_components = [
            ('life', 100.0),
            ('position', [0, 0], 'VectorComponent'),
            ('angle', 0),
            ('velocity', [0, 0], 'VectorComponent'),
            ('aiplayer',),
            ('toward', [0, 0], 'VectorComponent'),
            ('speed', 200),
            ('inventory', {}, 'InventoryComponent'),
            ('player',),
            ('bounding_box', (20, 20), 'VectorComponent'),
            ('render', 'normal'),
            ('sprite', 'player'),
            ('pushable',),
            ('weight', 100),
            ('collides',),
            ('anglerandom',)
        ]


    @loader.template
    class T_Barrel(EntityTemplate):
        editor_visible = True

        # The name of this template. Used when looking it up.
        name = 'barrel'

        # The group of this template. Used when looking a specific group of templates up.
        group = 'decoration.mobile'

        # A list of default components.
        default_components = [
            ('integrity', 100.0),
            ('position', [0, 0], 'VectorComponent'),
            ('angle', 0),
            ('velocity', [0, 0], 'VectorComponent'),
            ('inventory', {}, 'InventoryComponent'),
            ('pushable',),
            ('weight', 150),
            ('bounding_box', (38, 38), 'VectorComponent'),
            ('render', 'normal'),
            ('sprite', 'barrel'),
            ('pushable',),
            ('radius', 50),
            ('collides',),
            ('friction', 1.35),
            ('anglerandom',),
            ('sizerandom', 30),
        ]

    @loader.template
    class T_Ball(EntityTemplate):
        editor_visible = True

        # The name of this template. Used when looking it up.
        name = 'ball'

        # The group of this template. Used when looking a specific group of templates up.
        group = 'decoration.mobile'

        # A list of default components.
        default_components = [
            ('integrity', 30.0),
            ('position', [0, 0], 'VectorComponent'),
            ('angle', 0),
            ('velocity', [0, 0], 'VectorComponent'),
            ('inventory', {}, 'InventoryComponent'),
            ('pushable',),
            ('weight', 40),
            ('bounding_box', (18 * math.sqrt(2) / 2, 18 * math.sqrt(2) / 2), 'VectorComponent'),
            ('render', 'normal'),
            ('sprite', 'ball'),
            ('pushable',),
            ('radius', 18),
            ('collides',),
            ('friction', 0.4),
            ('anglerandom',),
            ('sizerandom', 4),
        ]


    @loader.template
    class T_Grass1(EntityTemplate):
        editor_visible = True
        name = 'grass1'
        group = 'decoration.static'

        default_components = [
            ('position', [0, 0], 'VectorComponent'),
            ('angle', 0),
            ('render', 'normal'),
            ('sprite', 'grass1'),
            ('radius', 60),
            ('sizerandom', 40),
            ('anglerandom',),
        ]


    @loader.template
    class T_Grass2(EntityTemplate):
        editor_visible = True
        name = 'grass2'
        group = 'decoration.static'

        default_components = [
            ('position', [0, 0], 'VectorComponent'),
            ('angle', 0),
            ('render', 'normal'),
            ('sprite', 'grass2'),
            ('radius', 60),
            ('sizerandom', 40),
            ('anglerandom',),
        ]


    @loader.template
    class T_Sign(EntityTemplate):
        editor_visible = True
        name = 'sign'
        group = 'decoration.dynamic'

        default_components = [
            ('position', [0, 0], 'VectorComponent'),
            ('angle', 0),
            ('render', 'normal'),
            ('sprite', 'sign'),
            ('radius', 50),
            ('sizerandom', 90),
            ('collides',),
            ('bounding_box', [120 * 50 / 200, 46 * 50 / 200], 'VectorComponent'),
            ('message', ''),
            ('anglerandom',),
            ('sizerandom', 25)
        ]


    @loader.system_type
    class S_SizeRandom(System):
        component_types = ['sizerandom']

        def on_spawned(self, event: EventContext, sizerandom, **kwargs):
            entity = event.source
            
            bump = self.game.random.uniform(-entity['sizerandom'].value, entity['sizerandom'].value)
            scale = (entity['radius'].value + bump) / entity['radius'].value
            entity['radius'].value = entity['radius'].value + bump

            if entity.has('bounding_box'):
                bb = ComponentVector(entity['bounding_box'])
                bb *= scale

            if 'weight' in entity:                
                entity['weight'].value *= scale

            else:
                entity['weight'] = DEFAULT_WEIGHT * scale ** 2


    @loader.system_type
    class S_AngleRandom(System):
        component_types = ['anglerandom']

        def on_spawned(self, event: EventContext, **kwargs):
            entity = event.source
            entity['angle'].value = self.game.random.uniform(0, math.pi * 2)


    @loader.system_type
    class S_Readable(System):
        component_types = ['message', 'position']

        def render(self, entity: Entity, window: pyglet.window.Window, position, message, **kwargs):
            pos = ComponentVector(position)
            dist = (self.manager.camera - pos).vsize()

            if dist < 150:
                alpha = 1 - dist / 150

                pos = get_pos(entity)
                x, y = self.manager.camera_transform(window, *pos)
                y += 60

                label = pyglet.text.Label(
                    message.value,
                    anchor_x = 'center',
                    anchor_y = 'center',
                    x = x,
                    y = y,
                    bold = True,
                    font_size=14 * self.manager.camera_zoom,
                    color=(190, 130, 30, int(255 * alpha)),
                    multiline=True,
                    width=window.width * 3 / 5,
                    align='center',
                )
                label.draw()

    @loader.template
    class T_FPSCounter(EntityTemplate):
        name = 'fpscounter'
        group = 'overlays'

        default_components = [
            ('fpscounter',)
        ]

    IMAGES = {}
        
    def load_sprite(name, path):
        img = pyglet.image.load(asset_path(path))
        mid = Vector((img.width / 2, img.height / 2))

        img.anchor_x = int(mid.x)
        img.anchor_y = int(mid.y)

        img.mid = mid

        IMAGES[name] = img
        return img

    @loader.routine('preload.yodine_data.sprites')
    def load_sprites(game):
        load_sprite('player', 'sprites/a_shitty_wallaby.png')
        load_sprite('barrel', 'sprites/barrel.png')
        load_sprite('grass1', 'sprites/grass1.png')
        load_sprite('grass2', 'sprites/grass2.png')
        load_sprite('leaves1', 'sprites/leaves1.png')
        load_sprite('leaves2', 'sprites/leaves2.png')
        load_sprite('localplayeranch1', 'sprites/branch1.png')
        load_sprite('branch2', 'sprites/branch2.png')
        load_sprite('sign', 'sprites/sign.png')
        load_sprite('ball', 'sprites/ball.png')

        print('Loaded sprites.')

    @loader.routine('get.yodine.sprites')
    def get_sprites():
        return IMAGES


    @loader.system_type
    class S_Collision(System):
        component_types = ['position', 'bounding_box', 'collides']

        def touches(self, entity, other_entity):
            pos1 = ComponentVector(entity['position'])
            pos2 = ComponentVector(other_entity['position'])

            box1 = ComponentVector(entity['bounding_box'])
            box2 = ComponentVector(other_entity['bounding_box'])

            wspan = box1.x + box2.x
            hspan = box1.y + box2.y

            return (
                abs(pos1.x - pos2.x) <= wspan / 2 and
                abs(pos1.y - pos2.y) <= hspan / 2
            )

        def get_weight(self, e):
            if 'weight' not in e:
                return DEFAULT_WEIGHT

            return e['weight'].value

        def get_velocity(self, e):
            if 'velocity' not in e:
                return Vector((0, 0))

            return ComponentVector(e['velocity'])

        def on_move(self, event: EventContext, start_pos, position, **kwargs):
            entity = event.source

            p = ComponentVector(position)
            dxy = p - start_pos

            for other_entity in self.manager:
                if other_entity.id != entity.id and other_entity.has('position', 'bounding_box', 'collides') and self.touches(entity, other_entity):
                    w1 = self.get_weight(entity)
                    w2 = self.get_weight(other_entity)

                    v1 = self.get_velocity(entity)

                    pos2 = ComponentVector(other_entity['position'])

                    if v1.sqsize() == 0:
                        continue

                    force = w1 * v1.vsize()
                    energy = (pos2 - p).unit() * force / (w1 + w2)

                    new_dxy = dxy * force / (w1 + w2)
                    new_vel_1 = v1 - energy

                    if 'velocity' in entity:
                        v1 << new_vel_1

                    else:
                        entity['position'] = start_pos + new_dxy
                        
                    p << start_pos

                    if other_entity.has('pushable', 'velocity'):
                        v2 = self.get_velocity(other_entity)
                        new_vel_2 = v2 + energy

                        v2 << new_vel_2

                        self.manager.emit(entity, 'push', other_entity)
                        self.manager.emit(other_entity, 'pushed', entity)

                    self.manager.emit(entity, 'bump', other_entity)
                    self.manager.emit(other_entity, 'bumped', entity)


    @loader.system_type
    class S_NormalRender(System):
        component_types = ['position', 'sprite']
        component_defaults = {'angle': 0}
        component_checks = {'render': 'normal'}

        def system_init(self):
            self.images = {}
            self.sprites = {}

            for r in self.manager.loader.routines['get.yodine.sprites']:
                self.images.update(r())

        def on_change_sprite(self, event: EventContext, new_sprite, **kwargs):
            entity = event.source

            if entity.id in self.sprites:
                self.sprites[entity.id].delete()
                
            self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[new_sprite.value])

        def render(self, entity: Entity, window: pyglet.window.Window, position, angle, sprite, **kwargs):
            vec = ComponentVector(position)
            sprite = self.sprites.setdefault(entity.id, pyglet.sprite.Sprite(self.images[sprite.value])) # type: pyglet.sprite.Sprite

            if (vec - entity.manager.camera).sqsize() < max(window.width, window.height) ** 2:
                sprite.visible = True

                newvec = Vector(entity.manager.camera_transform(window, vec.x, vec.y))

                sprite.x, sprite.y = newvec.x, newvec.y
                sprite.scale = self.manager.camera_zoom

                c_angle = self.manager.camera_angle
                sprite.rotation = -90 + math.degrees(-angle.value + c_angle)

                if 'radius' in entity:
                    rad = entity['radius'].value
                    sprite.scale /= max(sprite.image.width, sprite.image.height) / rad

                if 'scale' in entity:
                    scale = entity['scale'].value
                    sprite.scale *= scale

                sprite.draw()

            else:
                sprite.visible = False


    @loader.system_type
    class S_PlayerMovement(System):
        component_types = ['position', 'toward', 'velocity', 'player_move', 'speed', 'angle', 'localplayer']

        def on_mouse_move(self, event: EventContext, window, new_pos: Vector, pos_diff: Vector, position, velocity, speed, toward, angle, localplayer, **kwargs):
            if localplayer.value != self.game.id: return

            entity = event.source

            ang = math.atan2(
                new_pos.y - self.manager.game.window.height / 2,
                new_pos.x - self.manager.game.window.width / 2,
            )

            self.manager.game.net_emit(entity, ('player', 'aim'), ang)

        def on_player_aim(self, event: EventContext, ang, angle, **kwargs):
            entity = event.source

            if 'old_angle' in entity:
                angle.value += ang - entity['old_angle'].value

            entity['old_angle'] = ang

        def tick(self, entity: Entity, dtime: float, position, velocity, speed, toward, angle, localplayer, **kwargs):
            if localplayer.value != self.manager.game.id: return

            keyboard = self.manager.game.keyboard

            vel = ComponentVector(velocity)

            self.manager.set_camera(*position.value, angle.value, 1.3 / (1 + math.sqrt(vel.vsize()) / 90))

            tow = ComponentVector(toward)

            if keyboard[key.UP] or keyboard[key.W]:
                tow.x = 1

            elif keyboard[key.DOWN] or keyboard[key.S]:
                tow.x = -1

            if keyboard[key.LEFT] or keyboard[key.A]:
                tow.y = 1

            elif keyboard[key.RIGHT] or keyboard[key.D]:
                tow.y = -1

            if tow.sqsize() > 0:
                self.manager.game.net_emit(entity, ('player', 'thrust'), Vector(tow))

                tow.x = 0
                tow.y = 0

        def on_player_thrust(self, entity: Entity, tow: Vector, velocity, speed, angle,  **kwargs):
            delta_vel = tow.rotate(math.pi / 2 + angle.value).unit() * speed.value * self.manager.dtime
            vel = ComponentVector(velocity)
            vel += delta_vel


    @loader.system_type
    class S_AIMovement(System):
        component_types = ['position', 'toward', 'velocity', 'speed', 'angle', 'aiplayer']
        component_defaults = { 'ai_state': 'idle', 'delta_angle': 0 }

        def system_init(self):
            self.sight_distance = (35 * 4) ** 2

        def hit_wall(self, entity: Entity, col: str, ai_state, toward, delta_angle, **kwargs):
            tow = ComponentVector(toward)

            if tow.sqsize() == 0:
                cd = self.game.random.choice([1, -1])
                tow.y += cd
                delta_angle.value += cd

        def on_bump(self, event: EventContext, other, position, toward, delta_angle, velocity, **kwargs):
            assert 'position' in other

            vel = ComponentVector(velocity)
            pos = ComponentVector(position)
            pos2 = ComponentVector(other['position'])
            tow = ComponentVector(toward)

            tow.y += self.game.random.choice([1, -1])
            tow.x *= 0.8 / (pos - pos2).vsize()
            delta_angle.value -= tow.y * math.pi / 20

        def on_bumped(self, entity: Entity, other: Entity, ai_state, **kwargs):
            if ai_state.value != 'walking':
                ai_state.value = 'walking'

        def tick(self, entity: Entity, dtime: float, position, velocity, speed, toward, angle, ai_state, delta_angle, **kwargs):
            speed = speed.value
            vel = ComponentVector(velocity)
            tow = ComponentVector(toward)
            delta_angle.value /= 1 + 0.3 * dtime
            pos = ComponentVector(entity['position'])
            direc = Vector((
                math.cos(angle.value),
                math.sin(angle.value)
            ))

            if ai_state.value == 'idle':
                if tow.x != 0:
                    tow.x = 0

                if self.game.random.uniform(0, 1) ** dtime < 0.5:
                    delta_angle.value += self.game.random.uniform(-math.pi / 5, math.pi / 5)

                c = self.game.random.uniform(0, 1) ** dtime

                if c < 0.3:
                    ai_state.value = 'walking'

            elif ai_state.value == 'walking':
                if tow.x != 0.6:
                    tow.x = 0.6

                if self.game.random.uniform(0, 1) ** dtime < 0.5:
                    ai_state.value = 'idle'

            elif tow.x != 1:
                tow.x = 1

            if tow.sqsize() > 0:
                v = tow.rotate(math.pi / 2 + angle.value)

                if v.sqsize() > 1:
                    v = v.unit()

                vel += v * speed * dtime

                tow.x = 0
                tow.y = 0

            if delta_angle.value:
                angle.value += math.copysign(math.sqrt(abs(delta_angle.value)), delta_angle.value) * dtime
                delta_angle.value = 0


    @loader.component_type
    class InventoryComponent(Component, ItemContainer):
        def __init__(self, *args, **kwargs):
            ItemContainer.__init__(self)
            Component.__init__(self, *args, **kwargs)
            
        def get(self):
            return self.items

        def set(self, value):
            self.items = value

        def json_get(self):
            return self.items