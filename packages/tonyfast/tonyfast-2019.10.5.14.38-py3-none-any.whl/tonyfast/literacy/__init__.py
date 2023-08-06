with __import__('importnb').Notebook():
  try: from . import __doctest_post_run_cell, __interactive_markdown_cells
  except: import __doctest_post_run_cell, __interactive_markdown_cells