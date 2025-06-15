from typing import Any, Generator, List, Optional

import gradio

from facefusion import benchmarker, state_manager, wording
from facefusion.uis.core import get_ui_component

BENCHMARK_BENCHMARKS_DATAFRAME : Optional[gradio.Dataframe] = None
BENCHMARK_START_BUTTON : Optional[gradio.Button] = None


def render() -> None:
	global BENCHMARK_BENCHMARKS_DATAFRAME
	global BENCHMARK_START_BUTTON

	BENCHMARK_BENCHMARKS_DATAFRAME = gradio.Dataframe(
		headers =
		[
			'target_path',
			'benchmark_cycles',
			'average_run',
			'fastest_run',
			'slowest_run',
			'relative_fps'
		],
		datatype =
		[
			'str',
			'number',
			'number',
			'number',
			'number',
			'number'
		],
		show_label = False
	)
	BENCHMARK_START_BUTTON = gradio.Button(
		value = wording.get('uis.start_button'),
		variant = 'primary',
		size = 'sm'
	)


def listen() -> None:
	benchmark_resolutions_checkbox_group = get_ui_component('benchmark_resolutions_checkbox_group')
	benchmark_cycles_slider = get_ui_component('benchmark_cycles_slider')

	if benchmark_resolutions_checkbox_group and benchmark_cycles_slider:
		BENCHMARK_START_BUTTON.click(start, inputs = [ benchmark_resolutions_checkbox_group, benchmark_cycles_slider ], outputs = BENCHMARK_BENCHMARKS_DATAFRAME)


def start(benchmark_resolutions : List[str], benchmark_cycles : int) -> Generator[List[Any], None, None]:
	state_manager.set_item('benchmark_resolutions', benchmark_resolutions)
	state_manager.set_item('benchmark_cycles', benchmark_cycles)
	state_manager.sync_item('execution_providers')
	state_manager.sync_item('execution_thread_count')
	state_manager.sync_item('execution_queue_count')

	for benchmarks in benchmarker.run_with_progress():
		yield [ list(benchmark.values()) for benchmark in benchmarks ]
