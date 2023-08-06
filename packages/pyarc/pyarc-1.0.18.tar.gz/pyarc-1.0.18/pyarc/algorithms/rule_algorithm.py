class RuleBuilderAlgorithm:
    """Common ancestor for M1 and M2 Algorithms
    to provide common interface.
    """

    def __init__(self, rules, dataset):
        self.rules = rules
        self.dataset = dataset
        self.y = dataset.class_labels
        
    def update_class_distr(self, classdist, rule):
        return classdist - rule.class_cases_covered