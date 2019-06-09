from dataclasses import dataclass, field
from itertools import zip_longest
import sys
from textwrap import dedent
from typing import cast, Iterable, List, Optional, Tuple, Union

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
import requests


BOJ_PROBLEM_URL_TPL = 'https://www.acmicpc.net/problem/{}'


@dataclass
class Problem:
    title: str
    desc: str
    input: str
    output: str
    samples: List[Tuple[str, str]] = field(default_factory=list)


def print_usage() -> None:
    print('Usage:\n  boj2md <problem id>')


def fetch_problem_html(problem_id: str) -> str:
    r = requests.get(BOJ_PROBLEM_URL_TPL.format(problem_id))
    r.raise_for_status()
    return r.text


def html_to_text(bs: BeautifulSoup, selector: str) -> str:
    def parse_tag(tag: Union[NavigableString, Tag]) -> Optional[str]:
        if not tag.name:  # if tag is NavigableString
            return str(tag).strip() or None
        if tag.name == 'p':
            return '{}\n'.format(tag.text)
        elif tag.name == 'ul':
            child_string = '\n'.join(
                # Remove 'None' in list
                list(filter(lambda x: x is not None,
                            cast(List[str],
                                 [parse_tag(ctag) for ctag in tag.children])
                            ))
            )
            return '\n{}\n'.format(child_string)
        elif tag.name == 'li':
            return '- {}'.format(tag.text)
        else:
            return tag.text

    parsed_strings = []
    for tag in bs.select(selector)[0]:
        parsed_string = parse_tag(tag)
        if parsed_string is not None:
            parsed_strings.append(parsed_string)
    return '\n'.join(parsed_strings)


def pair_iter(iterable: Iterable[Tag]) -> Iterable[Tuple[Tag, Tag]]:
    return zip_longest(*([iter(iterable)]*2))


def parse_problem(html_doc: str) -> Problem:
    soup = BeautifulSoup(html_doc, 'html.parser')
    title = html_to_text(soup, '#problem_title')
    desc = html_to_text(soup, '#problem_description')
    _input = html_to_text(soup, '#problem_input')
    output = html_to_text(soup, '#problem_output')

    samples = []
    for sample_input, sample_output in pair_iter(soup.select('.sampledata')):
        samples.append((sample_input.text.strip(), sample_output.text.strip()))
    return Problem(title, desc, _input, output, samples)


def to_markdown(problem: Problem, problem_id: str) -> str:
    def samples_to_markdown(samples: List[Tuple[str, str]]) -> str:
        template = dedent('''\
                          ## 예제 입력 {index}

                          ```
                          {input}
                          ```

                          ## 예제 출력 {index}

                          ```
                          {output}
                          ```
                          ''')
        return '\n'.join(
            [template.format(index=idx+1,
                             input=sample_input,
                             output=sample_output)
             for idx, (sample_input, sample_output) in enumerate(samples)]
        )
    t = dedent('''\
        # {title}

        {url}

        {desc}

        ## 입력

        {input}

        ## 출력

        {output}

        {samples}
        ''')
    return t.format(
        title=problem.title,
        url=BOJ_PROBLEM_URL_TPL.format(problem_id),
        desc=problem.desc,
        input=problem.input,
        output=problem.output,
        samples=samples_to_markdown(problem.samples)
    )


def main() -> None:
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)
    problem_id = sys.argv[1]
    print(to_markdown(parse_problem(fetch_problem_html(problem_id)),
                      problem_id))


if __name__ == '__main__':
    main()
