---
name: Feature Implementation Template
about: A template for implementing a feature in the TPM repository.
title: 'Implementation: [FEATURE NAME]'
labels: implementation
assignees: ''

---

- [ ] **Copy the Template.** Go to the Feature Wiki and Copy/Paste the [Feature Template](https://github.com/Watts-Lab/team-process-map/wiki/Feature-Template-%5BCOPY-ME%5D) into a new page.

- [ ] **Fill out the Template.** Fill out the basic information for the feature in the template. Use the template to document your plan for implementation and major design decisions; if anything changes along the way, update the documentation as you go.

- [ ] **Create a new Feature file.** Create a new file in the folder `src/features`. The name of the file should be `NAME_features.py`, where NAME is the name of your feature.

- [ ] **Update the entery for your feature in `feature_dictionary.py`.** You can find the dictionary inside the `src/` folder.

- [ ] **Code your feature.** Write the code for the feature.

- [ ] **Evaluate/Unit Test.** Come up with a method of evaluating your feature. How do you know that the feature is 'correct?' For simple features, this may be trivial; for more complex ones, you may need to break down each sub-function and unit test them separately, or validate on external data. Add your unit tests to the `tests/` folder.