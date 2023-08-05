from typing import Dict

from sqlalchemy import Column, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from jinja2 import Template as JinjaTemplate
from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.orm import relationship


class MissingVariablesError(Exception):
    def __init__(self, message):
        self.message = message


class Template:
    id = Column(Integer, primary_key=True)
    template_text = Column(Text, nullable=False)
    variable_default_values = Column(JSONB)
    required_variables = Column(ARRAY(Text))

    @declared_attr
    def documents(self):
        return relationship('Document', back_populates="template")

    def jinja_template(self,template_config: Dict=None):
        template_config = template_config if template_config else {}
        return JinjaTemplate(self.template_text, **template_config)

    def render_template(self, variables: Dict, template_config: Dict=None) -> str:
        base_vars = self.variable_default_values if self.variable_default_values else {}
        all_vars = {
            **base_vars,
            **(variables if variables else {})
        }
        t = self.jinja_template(template_config)
        required_variables = self.required_variables if self.required_variables else {}
        if not set(required_variables).issubset(set(all_vars.keys())):
            missing_variables = set(base_vars) - set(all_vars.keys())
            raise MissingVariablesError(message=f"Missing variables: {' '.join(missing_variables)}")
        return t.render(**all_vars)
