import logging
from .. import weave_types as types
from ..api import op
from . import wb_domain_types as wdt
from ..wandb_client_api import wandb_gql_query
from ..language_features.tagging import tagged_value_type
from .. import engine_trace
from .. import errors
from .. import environment


def _wbgqlquery_output_type(input_types: dict[str, types.Type]) -> types.Type:
    ot = input_types["alias_list"]
    if isinstance(ot, types.Const) and isinstance(ot.val, list):
        return types.TypedDict({alias: types.TypedDict() for alias in ot.val})
    return types.Dict(types.String(), types.TypedDict({}))


# This op replaces all domain root ops in the graph during the compilation step.
# It executes a GQL query (that is constructed inside of `compile_domain.py`)
# and returns the results as a weave type.
@op(
    name="gqlroot-wbgqlquery",
    input_type={"query_str": types.String(), "alias_list": types.List(types.String())},
    output_type=_wbgqlquery_output_type,
    pure=False,
)
def wbgqlquery(query_str, alias_list):
    tracer = engine_trace.tracer()
    num_timeout_retries = environment.num_gql_timeout_retries()
    with tracer.trace("wbgqlquery:public_api"):
        logging.info("Executing GQL query: %s", query_str)
        gql_payload = wandb_gql_query(
            query_str, num_timeout_retries=num_timeout_retries
        )
    for alias in alias_list:
        if alias not in gql_payload:
            raise errors.WeaveGQLExecuteMissingAliasError(
                f"Alias {alias} not found in query results"
            )
    return gql_payload


def _querytoobj_output_type(input_types: dict[str, types.Type]) -> types.Type:
    ot = input_types["output_type"]
    if isinstance(ot, types.Const) and isinstance(ot.val, types.Type):
        return ot.val
    return types.Any()


@op(
    name="gqlroot-querytoobj",
    input_type={
        "result_dict": types.TypedDict({}),
        "result_key": types.String(),
        "output_type": types.TypeType(),
    },
    output_type=_querytoobj_output_type,
)
def querytoobj(result_dict, result_key, output_type):
    if isinstance(output_type, tagged_value_type.TaggedValueType):
        output_type = output_type.value
    if output_type.instance_class is None or not issubclass(
        output_type.instance_class, wdt.GQLTypeMixin
    ):
        raise ValueError(
            f"Invalid output type for gqlroot-querytoobj, must be a GQLTypeMixin, got {output_type}"
        )
    res_gql = result_dict[result_key]
    if res_gql == None:
        return None
    res = output_type.instance_class.from_gql(res_gql)
    return res
