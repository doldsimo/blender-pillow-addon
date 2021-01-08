import bpy
import ptvsd

from PIL import Image
from PIL import ImageOps


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


ptvsd.enable_attach()


class TexturOperationsParms(bpy.types.Operator, bpy.types.StringProperty):

    bl_idname = "textur.operations_parms"
    bl_label = "Change image with operations"
    bl_options = {'REGISTER', 'UNDO'}

    root_folder = bpy.props.StringProperty(
        name="File path",
        description="Some elaborate description",
        default="",
        maxlen=1024,
        subtype="FILE_PATH"
    )

    new_image_name = bpy.props.StringProperty(
        name="File name",
        description="Some elaborate description",
        default="",
        maxlen=1024
    )

    solarize_threshold = bpy.props.IntProperty(
        name="Solarize threshold",
        description="Solarize threshold",
        default=255,
        min=0,
        max=255
    )

    invert = bpy.props.BoolProperty(
        name='Invert',
        description='Invert image',
        default=False
    )

    greyscale = bpy.props.BoolProperty(
        name='Greyscale',
        description='Image in Greyscale',
        default=False
    )

    rotate = bpy.props.IntProperty(
        name="Rotate",
        description="Rotate in degree",
        default=0,
        min=0,
        max=360,
    )

    def execute(self, context):

        if(self.root_folder):
            imList = self.root_folder.rsplit("\\", 1)

            imPath = imList[0]
            fileOldName = imList[1]

            fileType = fileOldName.rsplit(".", 1)

            if(self.new_image_name):
                newPath = imPath + "\\" + self.new_image_name + "." + fileType[1]
                
                im = Image.open(self.root_folder)
                print(self.root_folder)
                im = ImageOps.solarize(im, self.solarize_threshold)
                if(self.greyscale):
                    im = ImageOps.grayscale(im)
                if(self.invert):
                    im = ImageOps.invert(im)
                im = im.rotate(self.rotate)
                im.save(newPath)

                mat = bpy.data.materials.new(name="New_Mat")
                mat.use_nodes = True
                bsdf = mat.node_tree.nodes["Principled BSDF"]
                texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
                texImage.image = bpy.data.images.load(newPath)
                mat.node_tree.links.new(
                    bsdf.inputs['Base Color'], texImage.outputs['Color'])
                ob = context.view_layer.objects.active

                # Assign it to object
                ob.data.materials[0] = mat
        return {'FINISHED'}


def register():
    print("Registering Textur Operations Parms")
    bpy.utils.register_class(TexturOperationsParms)
    # bpy.utils.register_class(OHA_QuickLink_Props)


def unregister():
    print("Unregistering Textur Operations Parms")
    bpy.utils.unregister_class(TexturOperationsParms)
    # bpy.utils.unregister_class(OHA_QuickLink_Props)
