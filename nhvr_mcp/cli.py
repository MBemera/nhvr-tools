"""CLI for NHVR tools."""

from __future__ import annotations

import asyncio

import click

from nhvr_mcp.tools import (
    get_accreditation_info,
    get_breach_categories,
    get_cor_duties,
    get_dimension_limits,
    get_fatigue_rules,
    get_hml_info,
    get_mass_limits,
    get_permit_types,
    get_speed_limits,
    scrape_page,
    search_regulations,
    search_vehicle_registration,
)


def run_async(coro):
    return asyncio.run(coro)


@click.group()
@click.option("--format", "output_format", default="markdown", type=click.Choice(["markdown", "json"]))
@click.pass_context
def cli(context: click.Context, output_format: str) -> None:
    context.ensure_object(dict)
    context.obj["output_format"] = output_format


@cli.group()
def fatigue() -> None:
    """Fatigue rules."""


@fatigue.command("rules")
@click.option("--scheme", default="standard", type=click.Choice(["standard", "bfm", "afm"]))
@click.pass_context
def fatigue_rules(context: click.Context, scheme: str) -> None:
    output_format = context.obj["output_format"]
    result = get_fatigue_rules(scheme=scheme, output_format=output_format)
    click.echo(result)


@cli.group()
def mass() -> None:
    """Mass limits."""


@mass.command("limits")
@click.option("--include-hml", is_flag=True, default=False)
@click.pass_context
def mass_limits(context: click.Context, include_hml: bool) -> None:
    output_format = context.obj["output_format"]
    result = get_mass_limits(include_hml=include_hml, output_format=output_format)
    click.echo(result)


@mass.command("hml")
@click.pass_context
def mass_hml(context: click.Context) -> None:
    output_format = context.obj["output_format"]
    result = get_hml_info(output_format=output_format)
    click.echo(result)


@cli.group()
def dimension() -> None:
    """Dimension limits."""


@dimension.command("limits")
@click.pass_context
def dimension_limits(context: click.Context) -> None:
    output_format = context.obj["output_format"]
    result = get_dimension_limits(output_format=output_format)
    click.echo(result)


@cli.group()
def breach() -> None:
    """Breach categories."""


@breach.command("categories")
@click.option("--type", "breach_type", default=None)
@click.pass_context
def breach_categories(context: click.Context, breach_type: str | None) -> None:
    output_format = context.obj["output_format"]
    result = get_breach_categories(breach_type=breach_type, output_format=output_format)
    click.echo(result)


@cli.command("speed")
@click.pass_context
def speed_limits(context: click.Context) -> None:
    output_format = context.obj["output_format"]
    result = get_speed_limits(output_format=output_format)
    click.echo(result)


@cli.group()
def cor() -> None:
    """Chain of Responsibility duties."""


@cor.command("duties")
@click.option("--role", default=None)
@click.pass_context
def cor_duties(context: click.Context, role: str | None) -> None:
    output_format = context.obj["output_format"]
    result = get_cor_duties(role=role, output_format=output_format)
    click.echo(result)


@cli.command("accreditation")
@click.option("--module", default=None)
@click.pass_context
def accreditation(context: click.Context, module: str | None) -> None:
    output_format = context.obj["output_format"]
    result = get_accreditation_info(module=module, output_format=output_format)
    click.echo(result)


@cli.command("permits")
@click.option("--type", "permit_type", default=None)
@click.pass_context
def permits(context: click.Context, permit_type: str | None) -> None:
    output_format = context.obj["output_format"]
    result = get_permit_types(permit_type=permit_type, output_format=output_format)
    click.echo(result)


@cli.command("rego")
@click.argument("plate_number")
@click.pass_context
def rego(context: click.Context, plate_number: str) -> None:
    output_format = context.obj["output_format"]
    result = run_async(search_vehicle_registration(plate_number=plate_number, output_format=output_format))
    click.echo(result)


@cli.command("search")
@click.argument("query")
@click.pass_context
def search(context: click.Context, query: str) -> None:
    output_format = context.obj["output_format"]
    result = run_async(search_regulations(query=query, output_format=output_format))
    click.echo(result)


@cli.command("scrape")
@click.argument("url")
@click.pass_context
def scrape(context: click.Context, url: str) -> None:
    output_format = context.obj["output_format"]
    result = run_async(scrape_page(url=url, output_format=output_format))
    click.echo(result)


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
