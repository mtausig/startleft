from networkx import DiGraph

from slp_tf.slp_tf.tfplan.tfplan_objects import TfplanComponent, TfplanOTM
from slp_tf.slp_tf.tfplan.transformers.hierarchy_calculator import HierarchyCalculator

# CHILD_TYPE: [PARENT_TYPE_1, PARENT_TYPE_2...]
PARENTS_TYPES_BY_CHILDREN_TYPE = {'aws_ecs_task_definition': ['aws_ecs_service']}


class TfplanChildrenCalculator(HierarchyCalculator):

    def __init__(self, otm: TfplanOTM, graph: DiGraph):
        super().__init__(otm, graph.reverse(copy=True))

    def _calculate_component_parents(self, component: TfplanComponent) -> [str]:
        if component.tf_type not in PARENTS_TYPES_BY_CHILDREN_TYPE:
            return []

        return self._find_parent_by_closest_relationship(
            component,
            self._get_parent_candidates(PARENTS_TYPES_BY_CHILDREN_TYPE[component.tf_type]))
