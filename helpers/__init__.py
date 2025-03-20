import logging
import os
import sys
from pathlib import Path
from warnings import simplefilter

import pandas as pd
from dotenv import dotenv_values, load_dotenv

# Global variable to track initialization status
initialization_successful = False


def _setup_notebook_path(notebook_path):
    """
    Add the directory containing the notebook to the Python path.

    Args:
        notebook_path (str): Path to the notebook file.

    """
    try:
        if not notebook_path:
            print("❌ Error: No notebook path provided")
            return

        # Get the directory containing the notebook
        notebook_dir = str(Path(notebook_path).resolve().parent)

        # Add the directory to the Python path
        if notebook_dir not in sys.path:
            sys.path.insert(0, notebook_dir)
            print("✅ Added notebook directory to Python path:")
            print(f"   {notebook_dir}")
            print("   You can now import modules from this directory")
        else:
            print("ℹ️ Notebook directory already in Python path:")
            print(f"   {notebook_dir}")
        return
    except Exception as e:
        print(f"❌ Error setting notebook path: {str(e)}")
        return


def _setup_environment():
    """Initialize the Course environment with all necessary settings."""
    global initialization_successful

    if initialization_successful:
        print("🔄 Environment already initialized. Skipping...")
        return

    print("🔄 Initializing Course environment...")

    # Set up autoreload to automatically reload modules when they change
    # This is equivalent to %load_ext autoreload and %autoreload 2 in Jupyter
    try:
        from IPython import get_ipython

        ipython = get_ipython()
        if ipython is not None:
            ipython.magic("load_ext autoreload")
            ipython.magic("autoreload 2")

            print(
                "🔁 Autoreload enabled: modules will reload automatically when changed"
            )
    except (ImportError, AttributeError):
        pass  # Not in IPython environment or IPython doesn't support magic

    # Make sure we don't get any deprecation warnings from mlflow
    simplefilter(action="ignore", category=FutureWarning)
    print("🔕 Suppressed future deprecation warnings")

    import mlflow

    # Set up logging
    logging.root.setLevel(logging.INFO)
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    logging.getLogger(__name__)
    print("📝 Logging configured")

    # Make sure pandas has doesn't truncate the output
    pd.set_option("display.max_colwidth", None)
    pd.options.display.max_rows = 4000
    print("📊 Pandas display settings configured for better output")

    # Load environment variables from .env file
    dotenv_path = Path(__file__).parent.parent / ".env"
    print(f"🔍 Looking for .env file at: {dotenv_path}")

    # First get the values from the .env file without setting them
    env_file_values = dotenv_values(dotenv_path=dotenv_path)

    # Then load the values into the environment
    if load_dotenv(dotenv_path=dotenv_path):
        print(f"✅ Successfully loaded environment variables from {dotenv_path}")

        # Check if any environment variables are empty
        empty_vars = []
        loaded_vars = []

        for key, _ in env_file_values.items():
            # Get the actual value from the environment (might be overridden)
            value = os.environ.get(key)

            if value:
                # Mask sensitive values
                masked_value = value
                if any(
                    s in key.lower() for s in ["key", "secret", "password", "token"]
                ):
                    masked_value = "****" + value[-4:] if len(value) > 8 else "****"

                if len(masked_value) > 10:
                    loaded_vars.append(f"{key}={masked_value[:5]}...")
                else:
                    loaded_vars.append(f"{key}={masked_value}")
            else:
                empty_vars.append(key)

        if loaded_vars:
            print(f"📋 Loaded variables: {', '.join(loaded_vars)}")

        if empty_vars:
            # Create a prominent but not overwhelming error message
            error_border = "=" * 80
            error_message = f"MISSING ENVIRONMENT VARIABLES: {', '.join(empty_vars)}"
            " " * ((80 - len(error_message)) // 2)

            print("\n")
            print(error_border)
            print(f"❌  {error_message}  ❌")
            print(error_border)
            print("\n")
            print(
                "🚨 You must set values for these variables in your .env file to continue"
            )
            print("🚨 Please check the .env.example file for the required format")
            print("🚨 After updating your .env file, restart your notebook or run:")
            print("    helpers.initialize()")
            print("\n")
            return
    else:
        # Create a prominent but not overwhelming error message for missing .env file
        error_border = "=" * 80
        error_message = "MISSING .env FILE"
        " " * ((80 - len(error_message)) // 2)

        print("\n")
        print(error_border)
        print(f"❌  {error_message}  ❌")
        print(error_border)
        print("\n")
        print("🚨 The .env file is missing from the project root directory")
        print("🚨 Please create a .env file based on the .env.example template")
        print("🚨 After creating your .env file, restart your notebook or run:")
        print("    helpers.initialize()")
        print("\n")
        return

    # Disable system metrics logging - we are not on a GPU-powered machine
    mlflow.disable_system_metrics_logging()
    print("⚙️ Disabled MLflow system metrics logging")

    # Disable mlflow tracking notebook display - it has bugs when used from VSCode
    mlflow.tracing.disable_notebook_display()
    print("📔 Disabled MLflow notebook display (avoids VSCode bugs)")

    # Print a final success message
    print("\n" + "=" * 80)
    print("🎉 All systems go! Your Course environment is ready for learning!")
    print("=" * 80)

    # Set the global flag to indicate successful initialization
    initialization_successful = True
    return


def initialize(notebook_path: str = None):
    """
    Initialize the environment and optionally set up the notebook path.

    This function handles both environment initialization and notebook path setup.
    It should be called at the beginning of your notebook or script.

    Args:
        notebook (str, optional): Path to the notebook file, typically
            provided by VS Code as __vsc_ipynb_file__. If provided,
            the directory containing the notebook will be added to the Python path.

    Returns:
        bool: True if initialization was successful, False otherwise.

    Example usage in a VS Code notebook:
    ```python
    import helpers
    helpers.initializer(notebook=__vsc_ipynb_file__)

    # Now you can import modules from the notebook's directory
    from textsummarizer import TextSummarizer
    ```
    """
    # First set up the notebook path
    if notebook_path:
        path_setup_success = _setup_notebook_path(notebook_path)
        if not path_setup_success:
            print("⚠️ Warning: Failed to set up notebook path")

    # Then initialize the environment
    env_setup_success = _setup_environment()

    return env_setup_success
