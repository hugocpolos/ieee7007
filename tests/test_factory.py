import pytest

from ieee7007.factory import Factory
from tests.fake_ontology import FakeOntology


def test_initialize_empty_factory():
    with pytest.raises(AttributeError):
        Factory(None)


def test_factory_with_fake_ontology():
    ontology = FakeOntology()
    f = Factory(ontology)

    # invalid classes
    assert f.get_factory_by_name('aaa') is None
    assert f.get_factory_by_name('foo') is None
    assert f.get_factory_by_name('') is None

    # valid classes
    assert f.get_factory_by_name('evmEventCausation') is not None
    assert f.get_factory_by_name('evmResponsibilityAscription') is not None
    assert f.get_factory_by_name('evmAscriptionJustification') is not None
    assert f.get_factory_by_name('evmGroundsForAscription') is not None
    assert f.get_factory_by_name('evmAgentAccountability') is not None
    assert f.get_factory_by_name('evmNormViolationIncident') is not None
    assert f.get_factory_by_name('evmEthicalBehaviorMonitor') is not None
    assert f.get_factory_by_name('evmNormViolation') is not None
    assert f.get_factory_by_name('evmSocioTechnologyGovernance') is not None
    assert f.get_factory_by_name('evmLiabilitySanction') is not None
    assert f.get_factory_by_name('evmLegalResponsibilityAscription') is not None
    assert f.get_factory_by_name('evmgovernance_levels') is not None
    assert f.get_factory_by_name('evmresponsibility_extent') is not None
    assert f.get_factory_by_name('evmAccountablePerson') is not None
    assert f.get_factory_by_name('evmDistributedResponsibility') is not None
    assert f.get_factory_by_name('evmEnumDataTypes') is not None
    assert f.get_factory_by_name('evmEthicalResponsibilityAscription') is not None
    assert f.get_factory_by_name('evmlegal_liabilities') is not None
    assert f.get_factory_by_name('nepAgent') is not None
    assert f.get_factory_by_name('nepAgentAction') is not None
    assert f.get_factory_by_name('nepGovernment') is not None
    assert f.get_factory_by_name('nepAgentRole') is not None
    assert f.get_factory_by_name('nepNorm') is not None
    assert f.get_factory_by_name('nepSituation') is not None
    assert f.get_factory_by_name('nepRobot') is not None
    assert f.get_factory_by_name('nepTeam') is not None
    assert f.get_factory_by_name('nepPlanAction') is not None
    assert f.get_factory_by_name('nepEthicalPrinciple') is not None
    assert f.get_factory_by_name('nepDerogation') is not None
    assert f.get_factory_by_name('nepAgentPlan') is not None
    assert f.get_factory_by_name('nepnorm_category') is not None
    assert f.get_factory_by_name('nepEthicalDilemma') is not None
    assert f.get_factory_by_name('nepEthicalTheory') is not None
    assert f.get_factory_by_name('nepSituationPlanRepertoire') is not None
    assert f.get_factory_by_name('nepTaskAssignment') is not None
    assert f.get_factory_by_name('nepSocialCollection') is not None
    assert f.get_factory_by_name('nepEnvironment') is not None
    assert f.get_factory_by_name('nepAnswer') is not None
    assert f.get_factory_by_name('nepQuery') is not None
    assert f.get_factory_by_name('nepActionRationale') is not None
    assert f.get_factory_by_name('nepDilemmaMitigationPrinciple') is not None
    assert f.get_factory_by_name('nepnorm_states') is not None
    assert f.get_factory_by_name('nepteam_types') is not None
    assert f.get_factory_by_name('nepCommunity') is not None
    assert f.get_factory_by_name('nepCompany') is not None
    assert f.get_factory_by_name('nepConsequentialistNorm') is not None
    assert f.get_factory_by_name('nepDeontologicalNorm') is not None
    assert f.get_factory_by_name('nepDepartment') is not None
    assert f.get_factory_by_name('nepEnumDataTypes') is not None
    assert f.get_factory_by_name('nepExplanation') is not None
    assert f.get_factory_by_name('nepObligation') is not None
    assert f.get_factory_by_name('nepOrganization') is not None
    assert f.get_factory_by_name('nepPermission') is not None
    assert f.get_factory_by_name('nepProhibition') is not None
    assert f.get_factory_by_name('nepVirtuousNorm') is not None
    assert f.get_factory_by_name('nepautonomous_action_principles') is not None
    assert f.get_factory_by_name('nepdilemma_mitigation_principles') is not None
    assert f.get_factory_by_name('nepethical_principles') is not None
    assert f.get_factory_by_name('nepethical_theories') is not None
    assert f.get_factory_by_name('tloAgentCommunication') is not None
    assert f.get_factory_by_name('tloMethod') is not None
    assert f.get_factory_by_name('tloAgent') is not None
    assert f.get_factory_by_name('tloProcess') is not None
    assert f.get_factory_by_name('tloPlan') is not None
    assert f.get_factory_by_name('tloInformationArtifact') is not None
    assert f.get_factory_by_name('tloRole') is not None
    assert f.get_factory_by_name('tloEnumDataTypes') is not None
    assert f.get_factory_by_name('tloContinuant') is not None
    assert f.get_factory_by_name('tloSituation') is not None
    assert f.get_factory_by_name('tloCollective') is not None
    assert f.get_factory_by_name('tloPhysical') is not None
    assert f.get_factory_by_name('tloAbstract') is not None
    assert f.get_factory_by_name('tloActionEvent') is not None
    assert f.get_factory_by_name('tloEntity') is not None
    assert f.get_factory_by_name('tloDescription') is not None
    assert f.get_factory_by_name('tloEvent') is not None
    assert f.get_factory_by_name('tloTime') is not None
    assert f.get_factory_by_name('tloevmObject') is not None
    assert f.get_factory_by_name('tloProperty') is not None
    assert f.get_factory_by_name('tloSpatioTemporalPlace') is not None
    assert f.get_factory_by_name('tloEnvironmentalEvent') is not None
    assert f.get_factory_by_name('tloAttribute') is not None
    assert f.get_factory_by_name('tloManner') is not None
    assert f.get_factory_by_name('tloOccurrent') is not None
    assert f.get_factory_by_name('tloInteractionProcess') is not None
    assert f.get_factory_by_name('tloSchema') is not None
    assert f.get_factory_by_name('tloSocialInteractionProcess') is not None
