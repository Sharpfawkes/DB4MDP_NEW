from import_export import resources
from .models import QualityMeasure, MDP, Task, Enrichment, Languages, Reference, AboutPage, Variants

# maybe everytime an import is made into the table, ask the user if they want to download the old version of the table prior to uploading.
'''3 columns in user interface. rows initially show paramater name. option to add new row to each row section of the table. (table within a table) and then select the value
for each parameter. Either include/exclude etc. All/any for each row of main table'''


# TEMPORARY SOLUTION FOUND
# set ids for each page instead of being continuous to go from 000-099 on first page, 100-199 on second and so on. Whenever new data is being saved, from the confirm page,
# retrieve all data that is new (or try to do everything highlight in green) using a post save signal or modifying the save method. And then add a button to the main layout file
# of the admin interface that retrieves and displays all changes and only when the admin asks to push these changes to overwrite the already existing ones will it run the command to
# either update files on the server or github (i don't know how docker works to display the webpage)

# DONE
# The issue now is that docker doesnt have a container for git i think. And again I dont know how this server works or what os commands it works with but if its Linux then possible
# git comes preinstalled and i can run commands from the shell. But if it accepts windows commands alone, then that means i would have to isntall git through the requirements file.
# But the git for windows container is not present in docker. Or maybe it is i have to check maybe with the support engineers. My only solution to this problem is like i suggested
# earlier you'll have to switch the postgres database to be run online. This will still let you use the improt-export features once i make the necessary changes.

# NOT POSSIBLE
# mobile responsive. CHeck user device (bookmarks) and then modify the menu accordingly


# making queries by creating new tables does not seem plausible. The reason for this is that if a new MDP is added to the main table, then a new column will have to be created using
# django-south but i dont want to have to use that unnecessarily. Instead it would be easier to iterate through a list of all attributes of the mdp returned and exclude comparison of
# only certain fields (whose exclusion will never change. If inclusion is used then it will require  hardcoding.) and compare it against the value desired i.e yes or null or some new value
# created.

# DONE
# check the migrations files and see how makemigrations and migrate work. Even though I'm using this online postgres db now it still seems to detect that some changes have been made to the
# properties of the tables which leads me to believe that the migrations files are affecting it and preserving the old model. Check if the migration  files can be deleted without any issues
# to resolve this problem


# work on including the pg pass file in the folder. I dont want the database password just stored in python code.

# DONE
# fixing the index on the models

# DONE
# You'll have to look into migration faking before you add the auto increment field or the model is not going to update.

# NOT REQUIRED
##Maybe instead of creating an auto incrementing field and modifying table data i could just query the mdp_id column from the database, obtain the largest id within it, then set
# the field mdp_id to be non-editable in the update sheet with the text equal to whatever is the largest id +1.

# Overriding views in the django admin interface

# DONE
# instead of rendering the table by columns, what I could do, atleast temporarily is find the number of items in each column. Iterate through them and then use a for loop counter. If length
# of column is less than the current counter index then insert <td></td> otherwise insert the next object. Also, instead of hard-coding the names of the columns go through the db and check
# the types of names (putting them into a set) and then set the table up that way.

# export to csv button needs to be fixed from the user end

# DONE
# Tasks basic renders automatically no hard code on the html web page. Also fixed the export csv option in the admin interface (was only exporting enrichment table earlier). Filters on admin
# page

# NEEDS TO BE SORTED
# For allowing the user to enter an option other than null/yes, have a free text field with buttons containing the available options below it. The filter on the main page is automatically
# taken care of by django and will update to include the new value.

# DONE
# work on fixing the error that shows up in the command prompt while making migrations

# NEEDS TO BE SORTED
# Make it such that if the user enters an invalid id in the url, they can't access the page or in content block 2 a paragraph is simply put specifying that you have tried to access an
# invalid mdp. Do this by checking if the pk specified is greater than largest or smaller than smallest number in the database.

# TEMPORARY SOLUTION FOUND
# Files that are created during running the docker container are going to be local to the container. Only the container will be able to see it but files will not actually be created in the
# system. In order for docker to actually create the files you'll need to look into mounting volumes and then copy files between the host and the container.

# about page modification. Contact as a footer, References dictionary make into a table. Connecting the references with the tables so every time a new ref is added, it updates in teh table.
# adding hyperlinks to navigate and also checking the paper to set up the tables again

# NOT NEEDED
# Notes from kenneth love `
# creating custom filtering methods (for the side bar in the django admin interface) other than the default ones provided by django (42:23)

# SEEMS UNNECESSARY
# import filter get column names and then select partitions (specified using variables) and assign each partition to a heading Table with property and verbose name and section.
# For example create a data type section and put all necessary property names under it. After getting the column headers from the main table, use the newly created table to find what
# properties to put in each section.

# remember that youve modified all ids

# fix references, tasks table and about page
# fix error of not detecting static images on the about page.
# Check how the tables can be linked, how to use many to one and m2m fields and also implement the toolboxes page from the supplementary pdf
# set parent_id to be a prepopulated field instead of user defined and make it non-editable
# Change the stupid verbose names in the tasks field to be placeholders instead
# linking everything and adding trackers to pages
# integrate references table
# create separate urls file for the mdp app
# add variant references

# Do you want to add sub tasks as visible on the main page or only accessible from parent task pages

# Add a clear button to clear all currently selected options
# Add a header field to each page to specify the data that could be included at the top of the page. No existing class modification but creation of a new class.

# talk about old site and what the point of the site is

# in styling for a set text decoration to none and instead set it so that on hover puts a background behind it with opacity of 0.5 or something
# put navbar in flexbox

# DONE
# /*Changes to be made
#    Convert the vertical nav bar into a horizontal one. 
#    When hovering over each hyperlink within the nav bar, let a bounding box appear and in the case where required
#    allow the user to choose from a drop-down between basic and advanced.
# */

# Put all queried data into drop down menus. Enclose data in a div and then set display to block WITH TRANSITION
# Replacing references ith a many to many or one to many field
# make options enlarge on hover instead of just background change
# set min-width parameter
# neon table?

# I dont think youll be able to see the references list in the mdp models because it is a manyto many field. I think the only think created is a one-one link
# between the two tables and no extra column within the MDP table
# update mathjax fields to be many to one and not mnay to many

# migration squaching
# https://www.techiediaries.com/squash-django-migrations/

# for quality basic and advanced
class QualityResource(resources.ModelResource):
    class Meta:
        model = QualityMeasure
        import_id_fields = ['measure_id']


class VariantResource(resources.ModelResource):
   class Meta:
       model = Variants
       import_id_fields=['variant_id']

# for mdp basic and advanced
class MDPResource(resources.ModelResource):
    # This file works alongside django-import-export. The import_id_fields is used when you want to explicitly
    # specify that an id field is already going to be present in the file that you will provide to import and it will
    # be named 'mdp_id'. If such a column won't be present remove the id_field line and the id will automatically be
    # assigned by postgres and used as the primary key for the data in the table.
    class Meta:
        model = MDP
        import_id_fields = ['mdp_id']


# for basic and advanced
class TaskResource(resources.ModelResource):
    class Meta:
        model = Task
        import_id_fields = ['task_id']


# for basic
class EnrichmentResource(resources.ModelResource):
    class Meta:
        model = Enrichment
        import_id_fields = ['enrichment_id']


class LanguagesResource(resources.ModelResource):
    class Meta:
        model = Languages
        import_id_fields = ['language_id']


# class RefResource(resources.ModelResource):
#     class Meta:
#         model = Reference
#         import_id_fields = ['reference_id']


class AboutResource(resources.ModelResource):
    class Meta:
        model = AboutPage
