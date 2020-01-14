from django.db import models
from django.contrib.admin.models import LogEntry
from django.core.files import File
# from .utils import run_on_save
# from django.db import connection
# import subprocess
# from django import forms
# from django.db.models.signals import post_save


file = open("new_changes.txt", "w")


# set the unique=true aprameter for those parts of the model apart from the primary key that need to be unique (name
# etc.) Youre going to have to use model save overriding instead of using a post save signal because the save signal
# gets called whenever data is pushed into the database i.e. even on start up def run_on_save(sender,instance,
# **kwargs): LogEntry.objects.all() file = open("new_changes.txt","w") file.write(changes)

# post_save.connect(run_on_save)

# Create your models here.

# instead of going through each individual class and changing their save methods, I'm just going to inherit in one
# class, change the save method and then inherit that class in all the remaining models.

# class ModdedModel(models.Model):
#    def save(self, *args, **kwargs):
#        changes_file = ("new_changes.txt","w")
#        content2 = LogEntry.objects.all()
#        changes_file.write(content2)
#        super(ModdedModel, self).save(*args,**kwargs)

class Reference(models.Model):
    # reference_id = models.AutoField(primary_key = True)
    citation = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f'[{self.id}] {self.citation.strip()}'


class HandlingAbility(models.Model):
    # technique_handling_ability = models.CharField(max_length=2000, label='Enter a description of how the technique
    # can handle the desired parameter')
    technique_handling_ability = models.CharField(max_length=2000)

    def __str__(self):
        return self.technique_handling_ability

    class Meta:
        verbose_name_plural = "Handling Abilities"


class EqnTypes(models.Model):
    equation_type = models.CharField(max_length=100)


class MathJaxFormulas(models.Model):
    mathjaxeqn = models.CharField(max_length=500, unique=True)
    # This next field is to make it easier while filtering in admin. Just in case the admin wants to group multiple
    # sets of formulas such as input space, output space separately. It won't impact display on the site.
    equation_type = models.ForeignKey(EqnTypes, on_delete=models.CASCADE, related_name='eqntype')

    def __str__(self):
        return f'{self.mathjaxeqn} - {self.equation_type}'

    class Meta:
        verbose_name_plural = "MathJax Formulae"


class Variants(models.Model):
    variant_id = models.AutoField(primary_key=True)
    variant_name = models.CharField(max_length=100, unique=True)
    variant_reference = models.ForeignKey(Reference, on_delete=models.CASCADE, related_name='variant_ref')

    def _unicode_(self):
        return '/%s/' % self.variant_name

    def get_absolute_url(self):
        return '/mdp/%s/' % self.variant_id

    def __str__(self):
        return self.variant_name


class MDP(models.Model):
    mdp_id = models.AutoField(primary_key=True)
    mdp_name = models.CharField('MDP short form', max_length=500, unique=True)
    mdp_fullname = models.CharField('MDP full form', max_length=500, unique=True)
    # dissimilarity = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, related_name='dissimilarity')
    # ordinal = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, related_name='ordinal')
    # cartesian = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, related_name='cartesian')
    # ne_structures = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, verbose_name="Neighbouring Structures",
    # related_name='ne_structures')
    # categorical = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, related_name='categorical')
    # linearity = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, related_name='linearity')
    # supervision = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, related_name='supervision')
    # multi_level = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, related_name='multi_level')
    # locality = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, related_name='locality')
    # steerability = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, related_name='steerability')
    # stability = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, related_name='stability')
    # out_of_core_data = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, related_name='out_of_core_data')
    # From here till the end constitutes the Taxonomy

    # From here uptil categorical are grouped as data types
    dissimilarity = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, related_name='dissimilarity',
                                      null=True)
    ordinal = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, related_name='ordinal', null=True)
    cartesian = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, related_name='cartesian', null=True)
    ne_structures = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, null=True,
                                      verbose_name="Neighbouring Structures",
                                      related_name='ne_structures')
    categorical = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, null=True, related_name='categorical')

    linearity = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, null=True, related_name='linearity')
    supervision = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, null=True, related_name='supervision')
    multi_level = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, null=True, related_name='multi_level')
    locality = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, null=True, related_name='locality')
    steerability = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, null=True, related_name='steerability')
    stability = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, null=True, related_name='stability')
    out_of_core_data = models.ForeignKey(HandlingAbility, on_delete=models.CASCADE, null=True,
                                         related_name='out_of_core_data')
    complexity = models.ForeignKey(MathJaxFormulas, on_delete=models.CASCADE, null=True,
                                   verbose_name='Complexity (MathJax)')

    # the reference list has been made a foreign key because in the paper, all the methods only have one reference
    # paper associated with them change to a many to many field if necessary
    reference_paper = models.ForeignKey(Reference, on_delete=models.CASCADE, null=True,
                                        verbose_name="Reference Paper")

    # Figure out how to work the placeholder text values for the next two fields from admin.py

    # In the paper, in the variants table, there are both references with just numbers as well as references with names.
    # Both have to displayed differently so I have created two different fields for them. tech_variants will take a
    # value from the list of variants in the variant table while variant_refs will just take a number which will
    # signify a particular reference.
    tech_variants = models.ManyToManyField(Variants, related_name='variantstab')
    variant_refs = models.ManyToManyField(Reference, related_name='mainvarref')

    description = models.CharField('Comments/Description', null=True, blank=True, max_length=2000)

    @property
    def projection_name(self):
        return f'{self.mdp_fullname} ({self.mdp_name.strip()})'

    # def queryset(self, request):
    #    qs = super(MyAdmin, self).queryset(request)
    #    qs = qs.order_by('mdp_id')
    #    return qs

    def _unicode_(self):
        return '/%s/' % self.mdp_name

    def get_absolute_url(self):
        return '/mdp/%s/' % self.mdp_id

    def __str__(self):
        return self.mdp_name

    class Meta:
        verbose_name_plural = "Projection Techniques"


class QMParameters(models.Model):
    parameter_option = models.CharField(max_length=200)

    def __str__(self):
        return self.parameter_option


class QualityMeasure(models.Model):
    measure_id = models.AutoField(primary_key=True)
    measure_name = models.CharField(max_length=100, unique=True)
    # Span
    local = models.ForeignKey(QMParameters, on_delete=models.CASCADE, related_name='local')
    glob = models.ForeignKey(QMParameters, on_delete=models.CASCADE, related_name='global')
    # Distortion Type
    dissimilarity = models.ForeignKey(QMParameters, on_delete=models.CASCADE, related_name='dissimilarity')
    correlation = models.ForeignKey(QMParameters, on_delete=models.CASCADE, related_name='correlation')
    probability = models.ForeignKey(QMParameters, on_delete=models.CASCADE, related_name='probability')
    rank = models.ForeignKey(QMParameters, on_delete=models.CASCADE, related_name='rank')
    geometric = models.ForeignKey(QMParameters, on_delete=models.CASCADE, related_name='geometric')
    set_difference = models.ForeignKey(QMParameters, on_delete=models.CASCADE, related_name='setdifference')
    homology = models.ForeignKey(QMParameters, on_delete=models.CASCADE, related_name='homology')
    # Output
    rangee = models.ForeignKey(MathJaxFormulas, on_delete=models.CASCADE, related_name='range')
    best = models.IntegerField('Best MDP')

    reference = models.ManyToManyField(Reference)

    description = models.CharField('Comments/Description', null=True, blank=True, max_length=2000)

    def __str__(self):
        return self.measure_name

    class Meta:
        verbose_name_plural = "Quality Measures"


class Toolboxes(models.Model):
    toolbox_id = models.AutoField(primary_key=True)
    toolbox_name = models.CharField('Toolbox Name', max_length=100, unique=True)
    description = models.CharField('Comments/Description', null=True, blank=True, max_length=2000)
    references = models.ManyToManyField(Reference, blank=True, null=True)

    def _unicode_(self):
        return '/%s/' % self.toolbox_name

    def get_absolute_url(self):
        return '/mdp/%s/' % self.toolbox_id

    def __str__(self):
        return self.toolbox_name

    class Meta:
        verbose_name_plural = "Toolboxes"


class Languages(models.Model):
    language_id = models.AutoField(primary_key=True)
    language_name = models.CharField('Programming Language', max_length=50, unique=True)
    reference_list = models.ManyToManyField(Reference, max_length=300)
    # Each language will have one or more toolboxes  associated with it as mentioned in the supplementary paper.
    toolbox_name = models.ManyToManyField(Toolboxes, max_length=200, blank=True)
    description = models.CharField('Comments/Description', null=True, blank=True, max_length=2000)

    def _unicode_(self):
        return '/%s/' % self.language_name

    def get_absolute_url(self):
        return '/mdp/%s/' % self.language_id

    def __str__(self):
        return self.language_name

    class Meta:
        verbose_name_plural = "Programming Languages"


class MDPsForLang(models.Model):
    mdp_id = models.AutoField(primary_key=True)
    mdp_name = models.CharField("MDP Name(s)", unique = True, max_length = 200)
    # For the circle_list, select the languages which are represented with black circles in the table in the
    # supplementary paper. Similar for the square_list, choose the ones with the blank square in the paper.
    circle_list = models.ManyToManyField(Languages, related_name="circles")
    square_list = models.ManyToManyField(Languages, related_name="sqs")
    reference_list = models.ManyToManyField(Reference, max_length=300)
    description = models.CharField('Comments/Description', null=True, blank=True, max_length=2000)

    def __str__(self):
        return self.mdp_name


class TaskType(models.Model):
    type_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.type_name


class MDPProps(models.Model):
    mdp_property = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.mdp_property


class BestMDP(models.Model):
    best_matching_mdp = models.CharField(max_length = 700, unique = True)

    def __str__(self):
        return self.best_matching_mdp


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100, unique=True)
    # main_task is true if the task is a parent task and false if it is one of the hyphenated tasks that comes under a parent.
    # Will be used to decide which ones to display on the page.
    main_task = models.BooleanField(default = True)
    input_space = models.ForeignKey(MathJaxFormulas, related_name='input_space', on_delete=models.CASCADE)
    output_space = models.ForeignKey(MathJaxFormulas, related_name='output_space', on_delete=models.CASCADE)
    #
    #actor_choices = [(x,)*2 for x in ["U", "M", "U&M"]]
    actor_choices = [("U", "User"), ("M", "Machine"), ("U&M", "User and Machine")]
    actor = models.CharField(max_length=100, choices=actor_choices, default="U")
    ts = models.CharField(max_length=100)

    best_mdp_list = models.ForeignKey(BestMDP, related_name='best_mdp', on_delete=models.CASCADE)
    task_property = models.ForeignKey(MDPProps, related_name='mdp_props', on_delete=models.CASCADE)

    # The parent id and child id will be used to represent the main task and the hyphen-bulleted list that occurs in some
    # sections of the table in the paper. The numbers section is used to specify those tasks that have stuff like .3. after
    # them in the paper. The vague name is because at the moment I don't know what they stand for.
    parent_id = models.ForeignKey("self", on_delete=models.CASCADE)
    child_id = models.ManyToManyField("self")
    numbers = models.ManyToManyField("self", verbose_name="Number(s)")

    reference_list = models.ForeignKey(Reference, on_delete=models.CASCADE)

    description = models.CharField('Comments/Description', null=True, blank=True, max_length=2000)

    def __str__(self):
        return self.task_name

    class Meta:
        verbose_name_plural = "Tasks"


class Enrichment(models.Model):
    enrichment_id = models.AutoField(primary_key=True)
    enrichment_name = models.CharField(max_length=100, unique=True)
    enrichment_type = models.CharField(max_length=100)
    references_type = models.CharField(max_length=100)
    description = models.CharField('Comments/Description', null=True, blank=True, max_length=2000)

    def __str__(self):
        return (self.enrichment_name + ' (' + str(self.enrichment_id) + ')')

    def save(self, *args, **kwargs):
        super(Enrichment, self).save(*args, **kwargs)
        with open("new_changes.txt", "w+") as changes_file:
            changes_file = File(changes_file)
            changes = LogEntry.objects.all()
            # print(changes)
            for change_made in changes:
                # print(change_made, changes)
                changes_file.write(str(change_made))
            changes_file.seek(0)
        # print(changes_file.read())

    class Meta:
        verbose_name_plural = "Enrichments"


class AboutPage(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    employee_of = models.CharField('Institute/Employer', max_length=100)
    email = models.EmailField('Email address', max_length=200)
    image_name = models.CharField('Image Name (New image to be saved in the static directory with the same name)',
                                  max_length=50, default="blank.png", blank=False)  # set default

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Team Data"
