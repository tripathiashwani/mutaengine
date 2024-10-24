from rest_framework import serializers
from .tasks import send_assignment_email_task , send_offer_letter_email_task
import os
from django.core.files.storage import default_storage
from django.conf import settings
from .models import JobApplicant, JobApplicantExtraField, AssignmentSubmission

from src.apps.company.models import Company

class JobApplicantExtraFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobApplicantExtraField
        exclude = ["job_applicant","is_deleted"]




class JobApplicantSerializer(serializers.ModelSerializer):
    job_applicant_extra_fields = JobApplicantExtraFieldSerializer(many=True, required=False)

    class Meta:
        model = JobApplicant
        exclude = ["is_deleted"]

    def create(self, validated_data):
        extra_fields_data = validated_data.pop('job_applicant_extra_fields', [])

        job_template = validated_data.get("job_template",None)

        if job_template is None:
            raise serializers.ValidationError("Job template is required")
        
        job_deadline = job_template.deadline

        from datetime import date
        current_date = date.today()
        if job_deadline < current_date:
            raise serializers.ValidationError("Application cannot be submiited: passed deadline")

        job_applicant = JobApplicant.objects.create(**validated_data)

        
        if extra_fields_data:
            for extra_field_data in extra_fields_data:
                JobApplicantExtraField.objects.create(**extra_field_data, job_applicant=job_applicant)

        
        request = self.context['request']
        # company_name = Company.objects.all().first().name
        company_name="Mutaengine"
        applicant_name = f"{job_applicant.first_name} {job_applicant.last_name}"
        to_email = job_applicant.email
        role = str(job_applicant.job_template.title ) 
        last_date = job_applicant.job_template.deadline 
        assignment_detail_link = request.data.get('assignment_detail_link')
        application_id = str(job_applicant.id)
         # Initialize paths
        html_template_relative_path = None
        resume_relative_path = None

        # Save uploaded HTML template file
        html_file = request.FILES.get('html_template')
        print(request.FILES)
        if html_file:
            try:
                html_file_path = os.path.join('templates', html_file.name)
                path = default_storage.save(html_file_path, html_file)
                html_template_relative_path = path
                print(f"HTML template saved at: {html_template_relative_path}")
            except Exception as e:
                print(f"Error saving HTML template: {e}")


        # Save uploaded resume file
        resume_file = request.FILES.get('resume')
        if resume_file:
            try:
                resume_file_path = os.path.join('resumes', resume_file.name)
                path = default_storage.save(resume_file_path, resume_file)
                resume_relative_path = path
                print(f"Resume saved at: {resume_relative_path}")
            except Exception as e:
                print(f"Error saving resume: {e}")

        # Pass relative paths to the Celery task
        send_assignment_email_task.apply_async(
            (str(company_name), applicant_name, to_email, role, last_date, assignment_detail_link, application_id, resume_relative_path, html_template_relative_path),
            countdown=3
        )
        job_applicant.assignment_sent=True
        job_applicant.save()
        return job_applicant


class AssignmentSubmissionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignmentSubmission
        exclude = ["is_deleted"]

    def create(self, validated_data):

        applicant_id=validated_data.get('applicant_id')
        
        try:
            application=JobApplicant.objects.get(id=applicant_id)
        except JobApplicant.DoesNotExist:
            raise serializers.ValidationError("Application not found")
        
        job_deadline = application.job_template.deadline

        from datetime import date
        current_date = date.today()
        if job_deadline < current_date:
            raise serializers.ValidationError("Assignment cannot be submiited: passed deadline")

        
        assignment_submission = AssignmentSubmission.objects.create(**validated_data)
        
        application.assignment_submitted=True
        role=str(application.job_template.title)
        company_name="Mutaengine"
        applicant_name = f"{application.first_name} {application.last_name}"
        to_email = str(application.email)
        html_template_relative_path = None
        resume_relative_path = None
        offer_letter_relative_path = None
        request = self.context['request']
        offer_details = request.data.get('offer_details')
        manager_name = request.data.get('manager_name')

        # Save uploaded HTML template file
        html_file = request.FILES.get('html_template')
        print(request.FILES)
        if html_file:
            try:
                html_file_path = os.path.join('templates', html_file.name)
                path = default_storage.save(html_file_path, html_file)
                html_template_relative_path = path
                print(f"HTML template saved at: {html_template_relative_path}")
            except Exception as e:
                print(f"Error saving HTML template: {e}")


        # Save uploaded resume file
        resume_file = request.FILES.get('resume')
        if resume_file:
            try:
                resume_file_path = os.path.join('resumes', resume_file.name)
                path = default_storage.save(resume_file_path, resume_file)
                resume_relative_path = path
                print(f"Resume saved at: {resume_relative_path}")
            except Exception as e:
                print(f"Error saving resume: {e}")
                
        offer_letter_file = request.FILES.get('offer_letter')
        if offer_letter_file:
            try:
                offer_letter_file_path = os.path.join('offer_letters', offer_letter_file.name)
                path = default_storage.save(offer_letter_file_path,offer_letter_file)
                offer_letter_relative_path = path
                print(f"offer_letter saved at: {offer_letter_relative_path}")
            except Exception as e:
                print(f"Error saving offer_letter: {e}")
        application.save()
        # company_name, applicant, to_email, role, offer_details, manager_name=None, resume_relative_path=None, offer_letter_relative_path=None, html_template_relative_path=None
        send_offer_letter_email_task.apply_async(
            (str(company_name), applicant_name, to_email, role,offer_details,manager_name, resume_relative_path, offer_letter_relative_path,html_template_relative_path),
            countdown=3
        )
        return assignment_submission
class OfferletterSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobApplicant
        fields = ['id', 'submitted_offer_letter']

    def validate(self, attrs):
        if not attrs.get('id'):
            raise serializers.ValidationError('Job applicant ID is required')

        if not attrs.get('submitted_offer_letter'):
            raise serializers.ValidationError('Signed Offer letter is required')
        return super().validate(attrs)