import common
import cpputils


def Settings():
    settings = cpputils.Settings()
    settings["cases"]["scenario"] = "Camel"
    settings["cases"]["test"] = "Camel"
    settings["scenarios file"] = "../scenarios/scenarios.h"
    return settings


def HelpSettings():
    settings = cpputils.HelpSettings()
    settings["scenarios file"] = "The path to the generated scenarios to include"
    return settings


def Generate(parsed, settings):
    scenarios = parsed[0]
    feature = parsed[1]
    buffer = """
// Other bespoke headers
#include "[[scenarios file]]"

// Third party headers
#include "CppUnitTest.h"

// Standard library headers
#include <iostream>
#include <memory>

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace [[rootnamespace]][[namespace]]
{
  TEST_CLASS([[className]])
  {
[[TestBody]]

    TEST_CLASS_INITIALIZE(ClassInitialize)
    {
      std::clog << "Entering [[featureName]]" << std::endl;
    }

    TEST_CLASS_CLEANUP(ClassCleanup)
    {
      std::clog << "Exiting [[featureName]]" << std::endl;
    }
  };
}
"""[1:]

    buffer = buffer.replace("[[scenarios file]]", settings["scenarios file"])

    namespace = cpputils.FeatureName(feature, settings["cases"]["namespace"])
    buffer = buffer.replace("[[rootnamespace]]", settings["rootnamespace"])
    buffer = buffer.replace("[[namespace]]", namespace)

    # Print the class
    featureName = cpputils.FeatureName(feature, settings["cases"]["class"])
    buffer = buffer.replace("[[featureName]]", featureName)
    className = common.Tokenise("Feature", settings["cases"]["class"])
    buffer = buffer.replace("[[className]]", className)

    decl = "    static void {0}({1})\n"
    altdecl = "    TEST_METHOD({0})\n"
    cpp = cpputils.Cpp(settings, decl, altdecl, "    ")
    testBody = common.TestBody(scenarios, settings, cpp)
    buffer = buffer.replace("[[TestBody]]", testBody)

    return buffer
