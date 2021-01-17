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
from PIL import ImageEnhance
import cv2 as cv
import numpy as np

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

    # Color correction
    red_value: bpy.props.FloatProperty(
        name="Red portion",
        description="Red portion factor",
        default=1,
        min=0,
        max=1,
        precision=2,
        step=1,
    )
    
    green_value: bpy.props.FloatProperty(
        name="Green portion",
        description="Green portion factor",
        default=1,
        min=0,
        max=1,
        precision=2,
        step=1,
    )
    
    blue_value: bpy.props.FloatProperty(
        name="Blue portion",
        description="Blue portion factor",
        default=1,
        min=0,
        max=1,
        precision=2,
        step=1,
    )     

    # Image correction
    brightness: bpy.props.FloatProperty(
        name="brightness",
        description="brightness factor",
        default=1,
        min=0.01,
        max=1,
        precision=2,
        step=1,
        update=UpdatedFunction
    )

    sharpness: bpy.props.FloatProperty(
        name="Sharpness",
        description="Sharpness factor",
        default=1,
        min=0.01,
        max=10,
        precision=2,
        step=1,
        update=UpdatedFunction
    )

    contrast: bpy.props.FloatProperty(
        name="contrast",
        description="contrast factor",
        default=1,
        min=0.01,
        max=10,
        precision=2,
        step=1,
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

    flip_vertically: bpy.props.BoolProperty(
        name='Flip vertically',
        description='Flip vertically',
        default=False,
        update=UpdatedFunction
    )

    flip_horizontally: bpy.props.BoolProperty(
        name='Flip horizontally',
        description='Flip horizontally',
        default=False,
        update=UpdatedFunction
    )

    scale_image: bpy.props.FloatProperty(
        name="Scale",
        description="Scale",
        default=1.0,
        min=0,
        max=2,
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
    # bl_context = "objectmode"

    @ classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "root_folder")
        layout.prop(mytool, "new_image_name")


class Color_Correction_Panel(Panel):
    bl_label = "Color Correction"
    bl_idname = "OBJECT_PT_custom_panel_color_correction"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Image Editing"
    # bl_context = "objectmode"

    @ classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "red_value")
        layout.prop(mytool, "green_value")
        layout.prop(mytool, "blue_value")
        layout.operator("apply.colorcorrection")


class Image_Correction_Panel(Panel):
    bl_label = "Image Correction"
    bl_idname = "OBJECT_PT_custom_panel_image_correction"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Image Editing"
    # bl_context = "objectmode"

    @ classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        # TODO: Add Correcturs

        layout.prop(mytool, "brightness")
        layout.prop(mytool, "sharpness")
        layout.prop(mytool, "contrast")


class Filter_Panel(Panel):
    bl_label = "Filters"
    bl_idname = "OBJECT_PT_custom_panel_filter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Image Editing"
    # bl_context = "objectmode"

    @ classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "black_And_White")
        if(mytool.black_And_White):
            layout.prop(mytool, "black_And_White_Thresh")
        layout.prop(mytool, "invert")
        layout.prop(mytool, "greyscale")


class Transformations_Panel(Panel):
    bl_label = "Transformations"
    bl_idname = "OBJECT_PT_custom_panel_transformations"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Image Editing"
    # bl_context = "objectmode"

    @ classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "rotate")
        layout.prop(mytool, "flip_vertically")
        layout.prop(mytool, "flip_horizontally")
        layout.prop(mytool, "scale_image")

class Magic_Wand_Panel(Panel):
    bl_label = "Magic Wand"
    bl_idname = "OBJECT_PT_custom_panel_Magic_Wand"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Image Editing"
    # bl_context = "objectmode"

    @ classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        if(mytool.root_folder and mytool.new_image_name):
            layout.operator("textur.magicwand")


# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------
class ApplyColorCorrection(Operator):
    bl_label = "Apply"
    bl_idname = "apply.colorcorrection"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
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
                
                # Color Correction
                [width,height]=im.size
                for x in range(width):
                    for y in range(height):
                        [r,g,b]=im.getpixel((x, y))
                        r = round(r * mytool.red_value)
                        if r > 255:
                            r = 255
                        if r < 0:
                            r = 0

                        g = round(g * mytool.green_value)
                        if g > 255:
                            g = 255
                        if g < 0:
                            g = 0

                        b = round(b * mytool.blue_value)
                        if b > 255:
                            b = 255
                        if b < 0:
                            b = 0
                        value = (r,g,b)
                        im.putpixel((x, y), value)


                im.save(newPath)

                ob = context.view_layer.objects.active
                # if(ob.active_material is None):
                print("New Material")
                mat = bpy.data.materials.new(name="New_Mat")
                mat.use_nodes = True
                bsdf = mat.node_tree.nodes["Principled BSDF"]
                texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
                texImage.image = bpy.data.images.load(newPath)
                mat.node_tree.links.new(
                    bsdf.inputs['Base Color'], texImage.outputs['Color'])
                # else:
                #     print("Existing Material")
                #     mat = ob.active_material
                #     mat.use_nodes = True
                #     bsdf = mat.node_tree.nodes["Principled BSDF"]
                #     texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
                #     texImage.image = bpy.data.images.load(newPath)
                #     mat.node_tree.links.new(
                #         bsdf.inputs['Base Color'], texImage.outputs['Color'])

                # Assign it to object
                ob.data.materials[0] = mat

        return {'FINISHED'}

class MagicWand(Operator):
    bl_label = "Open Magic Wand"
    bl_idname = "textur.magicwand"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        print("open Magic Wand")

        if(mytool.root_folder):
            imList = mytool.root_folder.rsplit("\\", 1)

            imPath = imList[0]
            fileOldName = imList[1]

            fileType = fileOldName.rsplit(".", 1)

            if(mytool.new_image_name):
                newPath = imPath + "\\" + \
                    mytool.new_image_name + "." + fileType[1]

                img = cv.imread(newPath)
                window = SelectionWindow(img)
                window.show()

        return {'FINISHED'}


class WM_OT_HelloWorld(Operator):
    bl_label = "Apply"
    bl_idname = "textur.pillow_image_editing"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        # print the values to the console
        # print("Data:")
        # print("Path:", mytool.root_folder)
        # print("New Image Name:", mytool.new_image_name)
        # print("Boolean_2:", "dfadsf")

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
                    
                # Image Correction
                if(mytool.brightness):
                    im = ImageEnhance.Brightness(im).enhance(mytool.brightness)
                if(mytool.sharpness):
                    im = ImageEnhance.Sharpness(im).enhance(mytool.sharpness)
                if(mytool.contrast):
                    im = ImageEnhance.Contrast(im).enhance(mytool.contrast)
                
                # Image Transformation
                if(mytool.flip_vertically):
                    im = ImageOps.flip(im)
                if(mytool.flip_horizontally):
                    im = ImageOps.mirror(im)
                im = ImageOps.scale(im, mytool.scale_image, Image.BICUBIC)
                im = im.rotate(mytool.rotate)


                im.save(newPath)

                ob = context.view_layer.objects.active
                # if(ob.active_material is None):
                print("New Material")
                mat = bpy.data.materials.new(name="New_Mat")
                mat.use_nodes = True
                bsdf = mat.node_tree.nodes["Principled BSDF"]
                texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
                texImage.image = bpy.data.images.load(newPath)
                mat.node_tree.links.new(
                    bsdf.inputs['Base Color'], texImage.outputs['Color'])
                # else:
                #     print("Existing Material")
                #     mat = ob.active_material
                #     mat.use_nodes = True
                #     bsdf = mat.node_tree.nodes["Principled BSDF"]
                #     texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
                #     texImage.image = bpy.data.images.load(newPath)
                #     mat.node_tree.links.new(
                #         bsdf.inputs['Base Color'], texImage.outputs['Color'])

                # Assign it to object
                ob.data.materials[0] = mat

        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------


SHIFT_KEY = cv.EVENT_FLAG_SHIFTKEY
ALT_KEY = cv.EVENT_FLAG_ALTKEY


def _find_exterior_contours(img):
    ret = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(ret) == 2:
        return ret[0]
    elif len(ret) == 3:
        return ret[1]
    raise Exception("Check the signature for `cv.findContours()`.")


class SelectionWindow:
    def __init__(self, img, name="Magic Wand Selector", connectivity=4, tolerance=32):
        self.name = name
        h, w = img.shape[:2]
        self.img = img
        self.mask = np.zeros((h, w), dtype=np.uint8)
        self._flood_mask = np.zeros((h + 2, w + 2), dtype=np.uint8)
        self._flood_fill_flags = (
            connectivity | cv.FLOODFILL_FIXED_RANGE | cv.FLOODFILL_MASK_ONLY | 255 << 8
        )  # 255 << 8 tells to fill with the value 255
        cv.namedWindow(self.name)
        self.tolerance = (tolerance,) * 3
        cv.createTrackbar(
            "Tolerance", self.name, tolerance, 255, self._trackbar_callback
        )
        cv.setMouseCallback(self.name, self._mouse_callback)

    def _trackbar_callback(self, pos):
        self.tolerance = (pos,) * 3

    def _mouse_callback(self, event, x, y, flags, *userdata):

        if event != cv.EVENT_LBUTTONDOWN:
            return

        modifier = flags & (ALT_KEY + SHIFT_KEY)

        self._flood_mask[:] = 0
        cv.floodFill(
            self.img,
            self._flood_mask,
            (x, y),
            0,
            self.tolerance,
            self.tolerance,
            self._flood_fill_flags,
        )
        flood_mask = self._flood_mask[1:-1, 1:-1].copy()

        if modifier == (ALT_KEY + SHIFT_KEY):
            self.mask = cv.bitwise_and(self.mask, flood_mask)
        elif modifier == SHIFT_KEY:
            self.mask = cv.bitwise_or(self.mask, flood_mask)
        elif modifier == ALT_KEY:
            self.mask = cv.bitwise_and(self.mask, cv.bitwise_not(flood_mask))
        else:
            self.mask = flood_mask

        self._update()

    def _update(self):
        """Updates an image in the already drawn window."""
        viz = self.img.copy()
        contours = _find_exterior_contours(self.mask)
        viz = cv.drawContours(
            viz, contours, -1, color=(255,) * 3, thickness=-1)
        viz = cv.addWeighted(self.img, 0.75, viz, 0.25, 0)
        viz = cv.drawContours(viz, contours, -1, color=(255,) * 3, thickness=1)

        self.mean, self.stddev = cv.meanStdDev(self.img, mask=self.mask)
        meanstr = "mean=({:.2f}, {:.2f}, {:.2f})".format(*self.mean[:, 0])
        stdstr = "std=({:.2f}, {:.2f}, {:.2f})".format(*self.stddev[:, 0])
        cv.imshow(self.name, viz)
        cv.displayStatusBar(self.name, ", ".join((meanstr, stdstr)))

    def show(self):
        """Draws a window with the supplied image."""
        self._update()
        print("Press [q] or [esc] to close the window.")
        while True:
            k = cv.waitKey() & 0xFF
            if k in (ord("q"), ord("\x1b")):
                cv.destroyWindow(self.name)
                break


classes = (
    AllProperties,
    WM_OT_HelloWorld,
    ApplyColorCorrection,
    MagicWand,
    Image_Panel,
    Color_Correction_Panel,
    Image_Correction_Panel,
    Filter_Panel,
    Transformations_Panel,
    Magic_Wand_Panel
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
