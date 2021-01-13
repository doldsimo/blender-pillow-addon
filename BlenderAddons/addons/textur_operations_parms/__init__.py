import bpy
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )


from PIL import Image
from PIL import ImageOps

from . import sepia

bl_info = {
    "name": "Textur operations parms",
    "author": "Simon Dold",
    "version": (1, 0, 0),
    "blender": (2, 90, 0),
    "description": "Change image with operations",
    "category": "Mesh",
    "support": "TESTING",
    "location": "View 3D > Edit Mode > Mesh",
}


# ------------------------------------------------------------------------
#   Properties
# ------------------------------------------------------------------------

def UpdatedFunction(self, context):
    print("-------------------In update func...-------------------")
    WM_OT_HelloWorld.execute(self, context)
    return


class AllProperties(PropertyGroup):

    # Load Image
    root_folder: bpy.props.StringProperty(
        name="Path",
        description="Some elaborate description",
        default="",
        maxlen=1024,
        subtype="FILE_PATH",
        update=UpdatedFunction
    )

    new_image_name: bpy.props.StringProperty(
        name="New name",
        description="Some elaborate description",
        default="",
        maxlen=500,
        update=UpdatedFunction
    )

    # Corrections
    solarize_threshold: bpy.props.IntProperty(
        name="Solarize threshold",
        description="Solarize threshold",
        default=255,
        min=0,
        max=255,
        update=UpdatedFunction
    )


    # Filters

    black_And_White: bpy.props.BoolProperty(
        name='Black/White',
        description='Black and White filter',
        default=False,
        update=UpdatedFunction
    )

    black_And_White_Thresh: bpy.props.IntProperty(
        name="Black/White threshold",
        description="Black/White threshold",
        default=100,
        min=0,
        max=255,
        update=UpdatedFunction
    )

    greyscale: bpy.props.BoolProperty(
        name='Greyscale',
        description='Image in Greyscale',
        default=False,
        update=UpdatedFunction
    )

    invert: bpy.props.BoolProperty(
        name='Invert',
        description='Invert image',
        default=False,
        update=UpdatedFunction
    )

    sepia: bpy.props.BoolProperty(
        name='Sepia',
        description='Sepia Filter',
        default=False,
        update=UpdatedFunction
    )

    # Transformations
    rotate: bpy.props.IntProperty(
        name="Rotate",
        description="Rotate in degree",
        default=0,
        min=0,
        max=360,
        update=UpdatedFunction
    )


# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------


class Image_Panel(Panel):
    bl_label = "Load Image"
    bl_idname = "OBJECT_PT_custom_panel_Image"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Image Editing"
    bl_context = "objectmode"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "root_folder")
        layout.prop(mytool, "new_image_name")


class Image_Correction_Panel(Panel):
    bl_label = "Correction"
    bl_idname = "OBJECT_PT_custom_panel_image_correction"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Image Editing"
    bl_context = "objectmode"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        # TODO: Add Correcturs

        layout.prop(mytool, "root_folder")


class Filter_Panel(Panel):
    bl_label = "Filters"
    bl_idname = "OBJECT_PT_custom_panel_filter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Image Editing"
    bl_context = "objectmode"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "black_And_White")
        layout.prop(mytool, "black_And_White_Thresh")
        layout.prop(mytool, "invert")
        layout.prop(mytool, "greyscale")

class Transformations_Panel(Panel):
    bl_label = "Transformations"
    bl_idname = "OBJECT_PT_custom_panel_transformations"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Image Editing"
    bl_context = "objectmode"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "rotate")
         
# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------


class WM_OT_HelloWorld(Operator):
    bl_label = "Apply"
    bl_idname = "textur.pillow_image_editing"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        # print the values to the console
        print("Data:")
        print("Path:", mytool.root_folder)
        print("New Image Name:", mytool.new_image_name)
        print("Boolean_2:", "dfadsf")

        if(mytool.root_folder):
            imList = mytool.root_folder.rsplit("\\", 1)

            imPath = imList[0]
            fileOldName = imList[1]

            fileType = fileOldName.rsplit(".", 1)

            if(mytool.new_image_name):
                newPath = imPath + "\\" + \
                    mytool.new_image_name + "." + fileType[1]

                im = Image.open(mytool.root_folder)
                print(mytool.root_folder)
                im = ImageOps.solarize(im, mytool.solarize_threshold)
                if(mytool.greyscale):
                    im = ImageOps.grayscale(im)
                if(mytool.invert):
                    im = ImageOps.invert(im)
                if(mytool.sepia):
                    im = sepia.convert_sepia(im)
                if(mytool.black_And_White):
                    thresh = mytool.black_And_White_Thresh
                    def fn(x): return 255 if x > thresh else 0
                    im = im.convert('L').point(fn, mode='1')

                im = im.rotate(mytool.rotate)
                im.save(newPath)

                ob = context.view_layer.objects.active
                if(ob.active_material is None):
                    print("New Material")
                    mat = bpy.data.materials.new(name="New_Mat")
                    mat.use_nodes = True
                    bsdf = mat.node_tree.nodes["Principled BSDF"]
                    texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
                    texImage.image = bpy.data.images.load(newPath)
                    mat.node_tree.links.new(
                        bsdf.inputs['Base Color'], texImage.outputs['Color'])
                else:
                    print("Existing Material")
                    mat = ob.active_material
                    mat.use_nodes = True
                    bsdf = mat.node_tree.nodes["Principled BSDF"]
                    texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
                    texImage.image = bpy.data.images.load(newPath)
                    mat.node_tree.links.new(
                        bsdf.inputs['Base Color'], texImage.outputs['Color'])

                # Assign it to object
                ob.data.materials[0] = mat

        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------


classes = (
    AllProperties,
    WM_OT_HelloWorld,
    Image_Panel,
    Image_Correction_Panel,
    Filter_Panel,
    Transformations_Panel
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tool = PointerProperty(type=AllProperties)
    print("Aktivate Pillow-Blender-Addon")


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool
    print("Deaktivate Pillow-Blender-Addon")


# if __name__ == "__main__":
#     register()
