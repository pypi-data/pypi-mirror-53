"""
Copyright 2018-2019
Dan Aukes, Cole Brauer

Extends the VoxelModel class with functions for generating linkages
"""

from voxelfuse.voxel_model import VoxelModel

class Linkage(VoxelModel):
    def insertTabs(self, template, x_coords, y_coords, rotation_increments):
        # Tab template should be 1 voxel thick and an odd number of voxels in length/width
        # Tab template should use only materials 1 and 2 (red and green)

        # Remove empty space and measure height of mode;
        self.fitWorkspace()
        z_len = len(self.voxels[0, 0, :])

        # Isolate two halves of tab template
        tab_p1 = template.isolateMaterial(1)
        tab_p2 = template.isolateMaterial(2)

        # Compute offsets for tab origin
        tab_l = int(len(template.voxels[:, 0, 0]) - 1)
        tab_w = int((len(template.voxels[0, :, 0]) - 1) / 2)

        new_model = Linkage.emptyLike(self)

        for i in range(len(x_coords)): # For each coordinate set
            for z in range(z_len): # For each layer
                r = rotation_increments[i] % 4

                # Get current tab coords and offset coords for measuring second material
                x = x_coords[i]
                y = y_coords[i]
                x2 = x_coords[i] + (r == 0) - (r == 2)
                y2 = y_coords[i] - (r == 1) + (r == 3)

                # Set material of tab based on base model materials
                tab_p1_mat = self.voxels[x, y, z]
                tab_p2_mat = self.voxels[x2, y2, z]
                tab_p1 = tab_p1.setMaterialVector(self.materials[tab_p1_mat])
                tab_p2 = tab_p2.setMaterialVector(self.materials[tab_p2_mat])

                # Combine tab halves
                tab_full = tab_p1.union(tab_p2)

                # Set coordinates where tab will be inserted
                x_new = x - ((r == 1) * tab_w) - ((r == 2) * tab_l) - ((r == 3) * tab_w)
                y_new = y - ((r == 0) * tab_w) - ((r == 1) * tab_l) - ((r == 2) * tab_w)
                z_new = z

                tab_full.coords = (x_new, y_new, z_new)

                # Rotate and add the tab to the new model
                new_model = new_model.union(tab_full.rotate90(r))

        # Add remaining voxels to the new model
        new_model = new_model.union(self)

        return new_model