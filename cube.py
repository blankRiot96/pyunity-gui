from pyunity import *

class Oscillator(Behaviour):
    a = 0
    speed = ShowInInspector(int, 5)
    renderer = ShowInInspector(MeshRenderer)
    def Update(self, dt):
        self.a += dt * self.speed / 10
        x = 255 * (1 - abs((self.a % 3 * 2) % 2 - 1))
        period = int(self.a % 3 * 2)
        if period == 0:
            color = Vector3(255, x, 0)
        elif period == 1:
            color = Vector3(x, 255, 0)
        elif period == 2:
            color = Vector3(0, 255, x)
        elif period == 3:
            color = Vector3(0, x, 255)
        elif period == 4:
            color = Vector3(x, 0, 255)
        elif period == 5:
            color = Vector3(255, 0, x)
        self.renderer.mat.color = Color(*color)

class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.eulerAngles += Vector3(0, 90, 135) * dt

scene = SceneManager.AddScene("Scene")
scene.mainCamera.transform.position = Vector3(0, 0, -10)

root = GameObject("Root")
root.AddComponent(Rotator)
scene.Add(root)

i = 0
for direction in [Vector3.up(), Vector3.right(), Vector3.forward()]:
    for parity in [-1, 1]:
        i += 1
        side = direction * parity
        go = GameObject("Side", root)
        renderer = go.AddComponent(MeshRenderer)
        renderer.mesh = Mesh.double_quad(2)
        renderer.mat = Material(Color(255, 0, 0))
        oscillator = go.AddComponent(Oscillator)
        oscillator.renderer = renderer
        oscillator.speed = i
        go.transform.localPosition = side
        if direction == Vector3.forward():
            angle = 0
        elif direction == Vector3.back():
            angle = 180
        else:
            angle = 90
        go.transform.localRotation = Quaternion.FromAxis(angle, Vector3.forward().cross(side))
        scene.Add(go)

SceneManager.LoadScene(scene)