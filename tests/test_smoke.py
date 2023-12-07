"""A test placeholder"""

import xml.etree.ElementTree as etree

import markdown

from jetblack_markdown.autodoc import AutodocExtension
from jetblack_markdown.latex2mathml import Latex2MathMLExtension


def test_smoketest():
    content = """

@[jetblack_markdown]

Something else
"""
    extension = AutodocExtension(class_from_init=True)
    output = markdown.markdown(content, extensions=[extension])
    assert output is not None


def test_etree():
    tree = etree.fromstring('<div>Hello</div>')
    print(tree)


def test_math():
    content = r"""Black (1976) Options on futures/forwards

* The discounted futures price $ F $,
* Strike price $ K $,
* Risk-free rate $ r $,
* Annual dividend yield $ q $,
* Time to maturity $ \tau = T - t $
* Volatility $ \sigma $.

Most of the formula use one or both of the following terms.

$$
d_1 = \frac{\ln(F/K) + (\sigma^2/2)T}{\sigma\sqrt{T}}
$$

$$
d_2 = \frac{\ln(F/K) - (\sigma^2/2)T}{\sigma\sqrt{T}} = d_1 - \sigma\sqrt{T}
$$

where N(.) is the cumulative normal distribution function.
"""

    extension = Latex2MathMLExtension()
    output = markdown.markdown(content, extensions=[extension])
    assert output is not None
