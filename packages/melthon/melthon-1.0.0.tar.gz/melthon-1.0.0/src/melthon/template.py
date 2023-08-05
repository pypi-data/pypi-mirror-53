import tempfile
from pathlib import Path

from mako.lookup import TemplateLookup


def render_templates(template_dir, output_dir, context):
    with tempfile.TemporaryDirectory() as tmp_dir:
        template_lookup = TemplateLookup(directories=[template_dir],
                                         module_directory=tmp_dir,
                                         output_encoding='utf-8',
                                         encoding_errors='replace')

        # For each .mako template
        for template_path in Path(template_dir).glob('*.mako'):
            if len(template_path.suffixes) >= 2 and template_path.suffixes[-2] == '.template':
                # Skip <PAGE NAME>.template.mako files
                continue
            template = template_lookup.get_template(str(template_path.name))
            output_path = Path(output_dir).joinpath(template_path.stem).with_suffix('.html')
            with output_path.open('wb') as rendered_page:
                rendered_page.write(template.render(**context))
