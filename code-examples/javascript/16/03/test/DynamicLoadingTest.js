const assert = require("assert");
require("./spec_helper");
const DynamicLoadingPage = require("../pages/DynamicLoadingPage");

describe("Dynamic Loading @deep", function() {
  beforeEach(function() {
    DynamicLoadingPage.load(this.driver);
  });

  it("hidden element", async function() {
    await DynamicLoadingPage.loadExample("1");
    assert(
      await DynamicLoadingPage.isFinishTextPresent(),
      true,
      "Finish text not displayed"
    );
  });

  it("rendered element", async function() {
    await DynamicLoadingPage.loadExample("2");
    assert(
      await DynamicLoadingPage.isFinishTextPresent(),
      true,
      "Finish text not displayed"
    );
  });
});