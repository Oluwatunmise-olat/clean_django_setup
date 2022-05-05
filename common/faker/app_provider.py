from faker.providers import BaseProvider


class CustomAppProvider(BaseProvider):
    def post_titles(self):
        titles = [
            "Design the solution",
            "Prepare for implementation",
            "Prepare the test/QA environment",
            "Install the product in the test/QA environment",
            "Schedule jobs",
            "Prepare the production environment",
            "Install the Health Monitor",
            "Create a solution maintenance plan",
        ]

        return self.random_element(titles)
