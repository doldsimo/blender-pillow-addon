import ptvsd
import bpy
from PIL import Image

bl_info = {
    "name": "Textur Pixel Add-on",
    "author": "Simon Dold",
    "version": (1, 0, 0),
    "blender": (2, 91, 0),
    "description": "Address individual pixels",
    "category": "Textur",
    "support": "TESTING",
    "location": "View 3D > Edit Mode > Material",
}

ptvsd.enable_attach()


class TexturPixelEdit(bpy.types.Operator):
    bl_idname = "textur.matrix_textur_pixel"
    bl_label = "Change pixels in image"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        im = Image.open("C:\\Users\\chris\\Desktop\\taylor-volek-space-orc-weak-male-04.jpg")
        im.show()

        width = im.size[0]
        height = im.size[1]

        for x in range(0, width):
            for y in range(0, height):
                if(y % 2) == 0 or (x % 2) == 0:
                    im.putpixel((x, y), (0, 0, 0))

        im.save("C:\\Users\\chris\\Desktop\\taylor-volek-space-orc-weak-male-04.jpg")
        im.show()

        mat = bpy.data.materials.new(name="New_Mat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
        texImage.image = bpy.data.images.load(
            "C:\\Users\\chris\\Desktop\\taylor-volek-space-orc-weak-male-04.jpg")
        mat.node_tree.links.new(
            bsdf.inputs['Base Color'], texImage.outputs['Color'])
        ob = context.view_layer.objects.active       # Assign it to object
        ob.data.materials[0] = mat

        print("Ausgefuehrt")

        return {'FINISHED'}


def register():
    print("Registering Textur Pixel Edit")
    bpy.utils.register_class(TexturPixelEdit)


def unregister():
    print("Unregistering Textur Pixel Edit")
    bpy.utils.unregister_class(TexturPixelEdit)
