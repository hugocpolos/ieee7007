class FakeOntoClass:
    def __init__(self, world, name):
        self._world = world
        self.name = name

    def __call__(self, individual_name):
        self._world.new_individual(individual_name)
        print("[{}] created individual {}".format(self.name, individual_name))


class FakeIndividual:
    def __init__(self, name):
        self.name = name


class FakeWorld:
    def __init__(self):
        self._individuals = list()

    def individuals(self):
        return self._individuals

    def new_individual(self, individual_name):
        self._individuals.append(FakeIndividual(individual_name))

    def classes(self):
        return [
            FakeOntoClass(self, 'evmEventCausation'),
            FakeOntoClass(self, 'evmResponsibilityAscription'),
            FakeOntoClass(self, 'evmAscriptionJustification'),
            FakeOntoClass(self, 'evmGroundsForAscription'),
            FakeOntoClass(self, 'evmAgentAccountability'),
            FakeOntoClass(self, 'evmNormViolationIncident'),
            FakeOntoClass(self, 'evmEthicalBehaviorMonitor'),
            FakeOntoClass(self, 'evmNormViolation'),
            FakeOntoClass(self, 'evmSocioTechnologyGovernance'),
            FakeOntoClass(self, 'evmLiabilitySanction'),
            FakeOntoClass(self, 'evmLegalResponsibilityAscription'),
            FakeOntoClass(self, 'evmgovernance_levels'),
            FakeOntoClass(self, 'evmresponsibility_extent'),
            FakeOntoClass(self, 'evmAccountablePerson'),
            FakeOntoClass(self, 'evmDistributedResponsibility'),
            FakeOntoClass(self, 'evmEnumDataTypes'),
            FakeOntoClass(self, 'evmEthicalResponsibilityAscription'),
            FakeOntoClass(self, 'evmlegal_liabilities'),
            FakeOntoClass(self, 'nepAgent'),
            FakeOntoClass(self, 'nepAgentAction'),
            FakeOntoClass(self, 'nepGovernment'),
            FakeOntoClass(self, 'nepAgentRole'),
            FakeOntoClass(self, 'nepNorm'),
            FakeOntoClass(self, 'nepSituation'),
            FakeOntoClass(self, 'nepRobot'),
            FakeOntoClass(self, 'nepTeam'),
            FakeOntoClass(self, 'nepPlanAction'),
            FakeOntoClass(self, 'nepEthicalPrinciple'),
            FakeOntoClass(self, 'nepDerogation'),
            FakeOntoClass(self, 'nepAgentPlan'),
            FakeOntoClass(self, 'nepnorm_category'),
            FakeOntoClass(self, 'nepEthicalDilemma'),
            FakeOntoClass(self, 'nepEthicalTheory'),
            FakeOntoClass(self, 'nepSituationPlanRepertoire'),
            FakeOntoClass(self, 'nepTaskAssignment'),
            FakeOntoClass(self, 'nepSocialCollection'),
            FakeOntoClass(self, 'nepEnvironment'),
            FakeOntoClass(self, 'nepAnswer'),
            FakeOntoClass(self, 'nepQuery'),
            FakeOntoClass(self, 'nepActionRationale'),
            FakeOntoClass(self, 'nepDilemmaMitigationPrinciple'),
            FakeOntoClass(self, 'nepnorm_states'),
            FakeOntoClass(self, 'nepteam_types'),
            FakeOntoClass(self, 'nepCommunity'),
            FakeOntoClass(self, 'nepCompany'),
            FakeOntoClass(self, 'nepConsequentialistNorm'),
            FakeOntoClass(self, 'nepDeontologicalNorm'),
            FakeOntoClass(self, 'nepDepartment'),
            FakeOntoClass(self, 'nepEnumDataTypes'),
            FakeOntoClass(self, 'nepExplanation'),
            FakeOntoClass(self, 'nepObligation'),
            FakeOntoClass(self, 'nepOrganization'),
            FakeOntoClass(self, 'nepPermission'),
            FakeOntoClass(self, 'nepProhibition'),
            FakeOntoClass(self, 'nepVirtuousNorm'),
            FakeOntoClass(self, 'nepautonomous_action_principles'),
            FakeOntoClass(self, 'nepdilemma_mitigation_principles'),
            FakeOntoClass(self, 'nepethical_principles'),
            FakeOntoClass(self, 'nepethical_theories'),
            FakeOntoClass(self, 'tloAgentCommunication'),
            FakeOntoClass(self, 'tloMethod'),
            FakeOntoClass(self, 'tloAgent'),
            FakeOntoClass(self, 'tloProcess'),
            FakeOntoClass(self, 'tloPlan'),
            FakeOntoClass(self, 'tloInformationArtifact'),
            FakeOntoClass(self, 'tloRole'),
            FakeOntoClass(self, 'tloEnumDataTypes'),
            FakeOntoClass(self, 'tloContinuant'),
            FakeOntoClass(self, 'tloSituation'),
            FakeOntoClass(self, 'tloCollective'),
            FakeOntoClass(self, 'tloPhysical'),
            FakeOntoClass(self, 'tloAbstract'),
            FakeOntoClass(self, 'tloActionEvent'),
            FakeOntoClass(self, 'tloEntity'),
            FakeOntoClass(self, 'tloDescription'),
            FakeOntoClass(self, 'tloEvent'),
            FakeOntoClass(self, 'tloTime'),
            FakeOntoClass(self, 'tloevmObject'),
            FakeOntoClass(self, 'tloProperty'),
            FakeOntoClass(self, 'tloSpatioTemporalPlace'),
            FakeOntoClass(self, 'tloEnvironmentalEvent'),
            FakeOntoClass(self, 'tloAttribute'),
            FakeOntoClass(self, 'tloManner'),
            FakeOntoClass(self, 'tloOccurrent'),
            FakeOntoClass(self, 'tloInteractionProcess'),
            FakeOntoClass(self, 'tloSchema'),
            FakeOntoClass(self, 'tloSocialInteractionProcess')
        ]


class FakeOntology:
    def __init__(self):
        self.world = FakeWorld()
