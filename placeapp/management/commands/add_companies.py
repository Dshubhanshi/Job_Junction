from django.core.management.base import BaseCommand
from placeapp.models import Company
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Add predefined companies to the database'

    def handle(self, *args, **options):
        # List of companies to be added
        companies = [
    {
        "name": "Infosys",
        "description": "A leading multinational corporation providing business consulting, information technology, and outsourcing services.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "info@infosys.com",
        "contact_phone": "080-98765432",
        "website": "https://www.infosys.com",
        "picture_path": "media/company_pictures/infosys.png",
    },
    {
        "name": "Wipro",
        "description": "A global leader in information technology, consulting, and business process services.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "contact@wipro.com",
        "contact_phone": "080-12345678",
        "website": "https://www.wipro.com",
        "picture_path": "media/company_pictures/wipro.png",
    },
    {
        "name": "Flipkart",
        "description": "India's leading e-commerce platform, headquartered in Bengaluru.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "support@flipkart.com",
        "contact_phone": "080-88888888",
        "website": "https://www.flipkart.com",
        "picture_path": "media/company_pictures/flipkart.png",
    },
    {
        "name": "Google India",
        "description": "The Indian arm of Google, focusing on search, advertising, and cloud computing.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "contact@google.co.in",
        "contact_phone": "080-22223333",
        "website": "https://www.google.co.in",
        "picture_path": "media/company_pictures/google.png",
    },
    {
        "name": "Microsoft India",
        "description": "The Indian subsidiary of Microsoft, providing cloud, AI, and software solutions.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "info@microsoft.co.in",
        "contact_phone": "080-44444444",
        "website": "https://www.microsoft.com/en-in",
        "picture_path": "media/company_pictures/microsoft.png",
    },
    {
        "name": "IBM India",
        "description": "A global technology and consulting company with a focus on AI, cloud computing, and cybersecurity.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "contact@ibm.in",
        "contact_phone": "080-55555555",
        "website": "https://www.ibm.com/in-en",
        "picture_path": "media/company_pictures/ibm.png",
    },
    {
        "name": "Intel India",
        "description": "The Indian branch of Intel Corporation, specializing in semiconductor manufacturing and technology solutions.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "info@intel.in",
        "contact_phone": "080-66666666",
        "website": "https://www.intel.in",
        "picture_path": "media/company_pictures/intel.png",
    },
    {
        "name": "Dell Technologies",
        "description": "A multinational computer technology company providing PCs, storage, and IT solutions.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "support@dell.co.in",
        "contact_phone": "080-77777777",
        "website": "https://www.dell.co.in",
        "picture_path": "media/company_pictures/dell.png",
    },
    {
        "name": "Amazon India",
        "description": "The Indian division of Amazon, offering e-commerce, cloud computing, and digital streaming services.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "info@amazon.in",
        "contact_phone": "080-55555555",
        "website": "https://www.amazon.in",
        "picture_path": "media/company_pictures/amazon.png",
    },
    {
        "name": "Oracle India",
        "description": "The Indian branch of Oracle Corporation, specializing in database software and enterprise solutions.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "contact@oracle.in",
        "contact_phone": "080-33334444",
        "website": "https://www.oracle.com/in",
        "picture_path": "media/company_pictures/oracle.png",
    },
    {
        "name": "Accenture India",
        "description": "A global consulting and professional services company with a focus on digital transformation.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "contact@accenture.co.in",
        "contact_phone": "080-23456789",
        "website": "https://www.accenture.com/in-en",
        "picture_path": "media/company_pictures/accenture.png",
    },
    {
        "name": "Cisco India",
        "description": "The Indian division of Cisco Systems, specializing in networking and cybersecurity solutions.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "support@cisco.co.in",
        "contact_phone": "080-99999999",
        "website": "https://www.cisco.com/c/en_in",
        "picture_path": "media/company_pictures/cisco.png",
    },
    {
        "name": "SAP Labs India",
        "description": "The Indian R&D division of SAP, focusing on enterprise software solutions.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "info@saplabs.co.in",
        "contact_phone": "080-12312312",
        "website": "https://www.sap.com/india",
        "picture_path": "media/company_pictures/sap.png",
    },
    {
        "name": "Mindtree",
        "description": "An Indian multinational information technology and outsourcing company headquartered in Bengaluru.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "contact@mindtree.com",
        "contact_phone": "080-45678901",
        "website": "https://www.mindtree.com",
        "picture_path": "media/company_pictures/mindtree.png",
    },
    {
        "name": "Goldman Sachs India",
        "description": "The Indian arm of Goldman Sachs, focusing on investment banking and financial services.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "support@goldmansachs.co.in",
        "contact_phone": "080-98765432",
        "website": "https://www.goldmansachs.com",
        "picture_path": "media/company_pictures/goldmansachs.png",
    },
    {
        "name": "Deloitte India",
        "description": "A global consulting and professional services company with a major office in Bengaluru.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "info@deloitte.co.in",
        "contact_phone": "080-87654321",
        "website": "https://www2.deloitte.com/in",
        "picture_path": "media/company_pictures/deloitte.png",
    },
    {
        "name": "Capgemini India",
        "description": "A global leader in consulting, digital transformation, and technology services.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "contact@capgemini.com",
        "contact_phone": "080-55554444",
        "website": "https://www.capgemini.com/in-en",
        "picture_path": "media/company_pictures/capgemini.png",
    },
    {
        "name": "EY India",
        "description": "One of the world's largest professional services networks, focusing on audit, tax, and advisory.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "contact@ey.com",
        "contact_phone": "080-66677788",
        "website": "https://www.ey.com/en_in",
        "picture_path": "media/company_pictures/ey.png",
    },
    {
        "name": "Adobe India",
        "description": "The Indian branch of Adobe, specializing in digital media and creative software.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "support@adobe.co.in",
        "contact_phone": "080-11112222",
        "website": "https://www.adobe.com/in",
        "picture_path": "media/company_pictures/adobe.png",
    },
    {
        "name": "Ola Cabs",
        "description": "India's leading ride-sharing and mobility service, headquartered in Bengaluru.",
        "location": "Bengaluru, Karnataka",
        "contact_email": "info@olacabs.com",
        "contact_phone": "080-43214321",
        "website": "https://www.olacabs.com",
        "picture_path": "media/company_pictures/ola.png",
    }
]


        # Adding each company to the database
        for company_data in companies:
            # Create a new company instance
            company = Company(
                name=company_data["name"],
                description=company_data["description"],
                location=company_data["location"],
                contact_email=company_data["contact_email"],
                contact_phone=company_data["contact_phone"],
                website=company_data["website"],
            )

            # Save the company to generate an ID
            company.save()

            # Add the company picture if it exists
            picture_path = company_data.get("picture_path")
            if picture_path and os.path.exists(picture_path):
                with open(picture_path, 'rb') as pic_file:
                    company.company_picture.save(os.path.basename(picture_path), File(pic_file), save=True)

            self.stdout.write(self.style.SUCCESS(f"Added {company.name}"))

        self.stdout.write(self.style.SUCCESS("All companies added successfully!"))
