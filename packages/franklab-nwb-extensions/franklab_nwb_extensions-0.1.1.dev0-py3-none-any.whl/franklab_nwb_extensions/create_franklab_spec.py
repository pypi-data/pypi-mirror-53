'''Create the specification for the Frank Lab NWB extension

NWB provides many basic datatypes, but we also need to represent lab-specific
information. NWB includes an 'extension' mechanism that allows labs to specify
their own data types and store them in valid NWB files. Extensions can also be
shared across groups working with similar types of data.

For overview documentation on extensions in PyNWB, see the
[Extensions Short Tutorial](
 https://pynwb.readthedocs.io/en/latest/tutorials/general/extensions.html) and
[Extensions Long Tutorial](
 https://pynwb.readthedocs.io/en/latest/extensions.html#extending-nwb).

Here we demonstrate the use of NWB Extensions through example.

Currently the Frank Lab extension includes data types for apparatuses in which
our animals perform experiments (i.e. tracks, mazes, sleep boxes, open field
arenas), and tasks that our animals are performing on those
apparatuses (i.e. free exploration, W-alternation, sleep).

The code in this notebook will generate two YAML (.yaml) files at the locations
defined in the 'namespace_path' and 'extension_path' variables below.
'''

import os

from pynwb.spec import (NWBAttributeSpec, NWBDatasetSpec, NWBGroupSpec,
                        NWBNamespaceBuilder)

from franklab_nwb_extensions.core import (extension_filename, namespace,
                                          namespace_path, yaml_dir)


def main():
    '''
    Create the specification using PyNWB helpers.
    Now we will create the specification ('draw up the blueprints') for the
    Frank Lab extension. The main entries in a spec file are Groups, Attributes
    and Datasets; PyNWB provides helpers that allow us to generate our spec
    files using these components.

    We primarily use the [NWBGroupSpec](https://pynwb.readthedocs.io/en/stable/pynwb.spec.html#pynwb.spec.NWBGroupSpec) # noqa
    class to help us create valid NWB groups. An NWB group is basically just a
    container that can have things like a name, attributes, datasets, and even
    nested groups. In fl_extension.py (where we implement this extension in
    Python), each of these groups will get its own Python class.

    We add items within a group using [NWBAttributeSpec]() and
    [NWBDatasetSpec](). An NWB attribute is just what it sounds like: a short
    piece of metadata defining some attribute, such as a "help" text. An NWB
    dataset is also pretty self-explanatory: it's just some data
    (numbers, text, etc.).

    As an example, the cell below describes the representation of a behavioral
    task, and will generate the following lines in the
    franklab.extensions.yaml file:
    ```
     - neurodata_type_def: Task
       neurodata_type_inc: NWBDataInterface
       doc: a behavioral task
       attributes:
       - name: name
         dtype: text
         doc: the name of this task
       - name: description
         dtype: text
         doc: description of this task
       - name: help
         dtype: text
         doc: help doc
         value: help value
    ```

    ---------------------------
    Task (i.e. free exploration, W-alternation, sleep)
    ------
    A Task consists simply of two attributes:
    - a name (i.e. W-alternation, sleep, free exploration)
    - a description of the task

    Note that Task inherits from something called NWBDataInterface.
    NWBDataInterface is a group in PyNWB representing basically any kind of
    data, and which we can store in the NWB file in a ProcessingModule.
    See create_franklab_nwbfile.ipynb for a discussion of Processing Modules.
    ---------------------------
'''
    task = NWBGroupSpec(neurodata_type_def='Task',
                        neurodata_type_inc='NWBDataInterface',
                        doc='a behavioral task',
                        attributes=[
                            NWBAttributeSpec(
                                name='name',
                                doc='the name of this task',
                                dtype='text'),
                            NWBAttributeSpec(
                                name='description',
                                doc='description of this task',
                                dtype='text'),
                            NWBAttributeSpec(
                                name='help',
                                doc='help doc',
                                dtype='text',
                                value='Behavioral Task')])

    # ---------------------------
    # Apparatus (i.e. tracks, mazes, sleep boxes, arenas)
    # --------
    # We represent the topology of apparatuses using a graph representation
    # (i.e. nodes and edges)
    # - Nodes represent a component of an apparatus that you'd like the ability
    # to refer
    #   (e.g. W-track arms, reward wells, novel object, open field components)
    # - Edges represent the topological connectivity of the nodes
    #   (i.e. there should be an edge between the left track arm and the left
    #   reward well)
    # In addition, all nodes will contain x/y coordinates that allow us to
    # reconstruct not just
    # the topology, but also the spatial geometry, of the apparatuses.
    #
    # Below, we will first define the nodes and edges. Finally we will define
    # the Apparatus itself
    # as a container that holds the nodes and edges as sub-groups.
    # ---------------------------

    # Node
    # -----
    # Abstract represention for any kind of node in the topological graph
    # We won't actually implement abstract nodes. Rather this is a parent group
    # from which our more specific types of nodes will inherit. Note that NWB
    # specifications have inheritance.
    # The quantity '*' means that we can have any number (0 or more) nodes.
    node = NWBGroupSpec(
        neurodata_type_def='Node',
        neurodata_type_inc='NWBDataInterface',
        doc='nodes in the graph',
        quantity='*',
        attributes=[NWBAttributeSpec(name='name',
                                     doc='the name of this node',
                                     dtype='text'),
                    NWBAttributeSpec(name='help',
                                     doc='help doc',
                                     dtype='text',
                                     value='Apparatus Node')])

    # Edge
    # -------
    # Edges between any two nodes in the graph.
    # An edge's only dataset is the name (string) of the two nodes that the
    # edge connects
    # Note that we don't actually include the nodes themselves, just their
    # names, in an edge.
    edge = NWBGroupSpec(
        neurodata_type_def='Edge',
        neurodata_type_inc='NWBDataInterface',
        doc='edges in the graph',
        quantity='*',
        datasets=[
            NWBDatasetSpec(
                doc='names of the nodes this edge connects',
                name='edge_nodes',
                dtype='text',
                dims=['first_node_name|second_node_name'],
                shape=[2])],
        attributes=[
            NWBAttributeSpec(
                name='help',
                doc='help doc',
                dtype='text',
                value='Apparatus Edge')])

    # Point Node
    # -----------
    # A node that represents a single 2D point in space (e.g. reward well,
    # novel object location)
    point_node = NWBGroupSpec(
        neurodata_type_def='PointNode',
        neurodata_type_inc='Node',
        doc='node representing a point in 2D space',
        quantity='*',
        datasets=[NWBDatasetSpec(doc='x/y coordinate of this 2D point',
                                 name='coords',
                                 dtype='float',
                                 dims=['num_coords',
                                       'x_vals|y_vals'],
                                 shape=[1, 2])],
        attributes=[NWBAttributeSpec(name='help',
                                     doc='help doc',
                                     dtype='text',
                                     value='Apparatus Point')])

    # Segment Node
    # -------------
    # A node that represents a linear segement in 2D space, defined by its
    # start and end points
    # (e.g. a single arm of W-track maze)
    segment_node = NWBGroupSpec(
        neurodata_type_def='SegmentNode',
        neurodata_type_inc='Node',
        doc=('node representing a 2D linear segment defined by its start and'
             'end points'),
        quantity='*',
        datasets=[
            NWBDatasetSpec(doc=('x/y coordinates of the start and end points '
                                'of this segment'),
                           name='coords',
                           dtype='float',
                           dims=['num_coords', 'x_vals|y_vals'],
                           shape=[2, 2])],
        attributes=[
            NWBAttributeSpec(name='help',
                             doc='help doc',
                             dtype='text', value='Apparatus Segment')])

    # Polygon Node
    # -------------
    # A node that represents a polygon area (e.g. open field, sleep box)
    # A polygon is defined by its external vertices and, optionally, by
    # any interior points of interest (e.g. interior wells, objects)
    polygon_node = NWBGroupSpec(
        neurodata_type_def='PolygonNode',
        neurodata_type_inc='Node',
        doc='node representing a 2D polygon area',
        quantity='*',
        datasets=[
            NWBDatasetSpec(
                doc='x/y coordinates of the exterior points of this polygon',
                name='coords',
                dtype='float',
                dims=['num_coords', 'x_vals|y_vals'],
                shape=['null', 2]),
            NWBDatasetSpec(
                doc='x/y coordinates of interior points inside this polygon',
                name='interior_coords',
                dtype='float',
                quantity='?',
                dims=['num_coords',
                      'x_vals|y_vals'],
                shape=['null', 2])],
        attributes=[
            NWBAttributeSpec(name='help',
                             doc='help doc',
                             dtype='text',
                             value='Apparatus Polygon')])

    # Apparatus
    # -------------
    # Finally, we define the apparatus itself.
    # It is has two sub-groups: nodes and edges.
    apparatus = NWBGroupSpec(
        neurodata_type_def='Apparatus',
        neurodata_type_inc='NWBDataInterface',
        doc='a graph of nodes and edges',
        quantity='*',
        groups=[node, edge],
        attributes=[
            NWBAttributeSpec(name='name',
                             doc='the name of this apparatus',
                             dtype='text'),
            NWBAttributeSpec(name='help',
                             doc='help doc',
                             dtype='text',
                             value='Behavioral Apparatus')])

    # ### Save the extension specification
    # The specification consists of two YAML (.yaml) files: one for the actual
    # blueprint and one for the namespace. In a world with many blueprints, we
    # need namespaces to effectively categorize/store them, like the drawers of
    # an architect's filing cabinet.

    namespace_builder = NWBNamespaceBuilder(
        f'{namespace} extensions', namespace)
    namespace_builder.add_spec(extension_filename, apparatus)
    namespace_builder.add_spec(extension_filename, task)
    namespace_builder.add_spec(extension_filename, point_node)
    namespace_builder.add_spec(extension_filename, segment_node)
    namespace_builder.add_spec(extension_filename, polygon_node)

    # Bug: NamespaceBuilder.add_spec creates the .extensions.yaml file in the
    # current directory (it errors if you pass in a file path containing '/'
    # to add_spec, above.)
    old_cwd = os.getcwd()
    os.chdir(yaml_dir)
    namespace_builder.export(namespace_path)
    os.chdir(old_cwd)


if __name__ == '__main__':
    main()
