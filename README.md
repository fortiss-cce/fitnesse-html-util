# FitNesse Html Util

This repository contains the `HtmlUtil.java` class from Robert C. Martin's Clean Code handbook (p. 32) or rather
from [FitNesse](https://github.com/unclebob/fitnesse/).

We use this project as a starting point for a fist simple refactoring task on function-level.

## How to build and run the FitNesse Html Util

### Required technologies

To run the application, the following should be installed:

* [git](https://git-scm.com/downloads)
* JDK (e.g., [AdoptOpenJDK](https://adoptopenjdk.net/))
* Optionally, [Apache Maven](https://maven.apache.org/install.html)

### Run from source

In the command line, run the following:

```shell
git clone https://github.com/fortiss-cce/fitnesse-html-util.git
cd fitnesse-html-util
./mvnw clean install
```

## Task

1. Create a fork of this repository
2. Try to understand [HtmlUtil.java](./src/main/java/HtmlUtil.java)
   and [HtmlUtilTest.java](./src/test/java/HtmlUtilTest.java)
3. Refactor the [HtmlUtil.java](./src/main/java/HtmlUtil.java) to the best of your belief
4. Create a pull request to submit you proposals
